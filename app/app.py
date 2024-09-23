```python
from flask import Flask, request, jsonify
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
    return jsonify([{
        'id': doc.id,
        'document_type': doc.document_type,
        'upload_date': doc.upload_date,
        'status': doc.status,
        'comments': doc.comments,
        'verification_result': doc.verification_result
    } for doc in documents])

@app.route('/documents/<int:document_id>/verify', methods=['POST'])
@login_required
def verify_document(document_id):
    if not current_user.is_loan_officer:
        return jsonify({'error': 'Unauthorized access'}), 403
    data = request.json
    document = Document.query.get(document_id)
    document.status = data.get('status', document.status)
    document.comments = data.get('comments', document.comments)
    db.session.commit()
    return jsonify({'message': 'Document updated successfully'})

@app.route('/documents/<int:document_id>/automate_verify', methods=['POST'])
@login_required
def automate_verify_document(document_id):
    if not current_user.is_loan_officer:
        return jsonify({'error': 'Unauthorized access'}), 403
    document = Document.query.get(document_id)
    response = requests.post('https://third-party-verification-service.com/verify', json={'document': document})
    verification_result = response.json().get('result')
    document.verification_result = verification_result
    db.session.commit()
    return jsonify({'verification_result': verification_result})

@app.route('/loan_applications/<int:loan_application_id>/update_status', methods=['POST'])
@login_required
def update_loan_application_status(loan_application_id):
    if not current_user.is_loan_officer:
        return jsonify({'error': 'Unauthorized access'}), 403
    loan_application = LoanApplication.query.get(loan_application_id)
    documents = Document.query.filter_by(loan_application_id=loan_application_id).all()
    if all(doc.status == 'verified' for doc in documents):
        loan_application.status = 'verified'
    elif any(doc.status == 'rejected' for doc in documents):
        loan_application.status = 'rejected'
    else:
        loan_application.status = 'pending'
    db.session.commit()
    # Notify customer via email or in-app notification
    return jsonify({'message': 'Loan application status updated'})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
```