```python
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, current_user
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///loan_applications.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)
login_manager = LoginManager(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_loan_officer = db.Column(db.Boolean, default=False)

class LoanApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_email = db.Column(db.String(150), nullable=False)
    status = db.Column(db.String(50), default='pending')

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loan_application_id = db.Column(db.Integer, db.ForeignKey('loan_application.id'), nullable=False)
    document_type = db.Column(db.String(50), nullable=False)
    upload_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), default='pending')
    comments = db.Column(db.Text, nullable=True)
    verification_result = db.Column(db.String(50), nullable=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/documents/<int:loan_application_id>', methods=['GET'])
@login_required
def get_documents(loan_application_id):
    if not current_user.is_loan_officer:
        return jsonify({'error': 'Unauthorized access'}), 403
    documents = Document.query.filter_by(loan_application_id=loan_application_id).all()
    return render_template('documents.html', documents=documents)

@app.route('/verify_document/<int:document_id>', methods=['POST'])
@login_required
def verify_document(document_id):
    if not current_user.is_loan_officer:
        return jsonify({'error': 'Unauthorized access'}), 403
    document = Document.query.get_or_404(document_id)
    data = request.json
    document.status = data.get('status')
    document.comments = data.get('comments')
    db.session.commit()
    update_loan_application_status(document.loan_application_id)
    return jsonify({'message': 'Document updated successfully'})

def update_loan_application_status(loan_application_id):
    documents = Document.query.filter_by(loan_application_id=loan_application_id).all()
    statuses = [doc.status for doc in documents]
    if all(status == 'verified' for status in statuses):
        status = 'verified'
    elif any(status == 'rejected' for status in statuses):
        status = 'rejected'
    else:
        status = 'pending'
    loan_application = LoanApplication.query.get(loan_application_id)
    loan_application.status = status
    db.session.commit()
    notify_customer(loan_application.customer_email, status)

def notify_customer(email, status):
    # Placeholder for email or in-app notification logic
    pass

@app.route('/automated_verification/<int:document_id>', methods=['POST'])
@login_required
def automated_verification(document_id):
    if not current_user.is_loan_officer:
        return jsonify({'error': 'Unauthorized access'}), 403
    document = Document.query.get_or_404(document_id)
    verification_result = requests.post('https://third-party-verification-service.com/verify', json={'document': document})
    document.verification_result = verification_result.json().get('result')
    db.session.commit()
    return jsonify({'message': 'Automated verification completed', 'result': document.verification_result})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
```