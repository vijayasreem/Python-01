Sure! Here's an example of a Python Flask API code that handles the user story you provided:

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for loan applications
loan_applications = []

@app.route('/apply', methods=['POST'])
def apply_loan():
    data = request.json

    # Validate incoming request data
    if not all(key in data for key in ['personal_details', 'income_details', 'employment_details']):
        return jsonify({'error': 'Invalid request data.'}), 400

    # Save the loan application
    loan_applications.append(data)

    # Send confirmation to the customer
    return jsonify({'message': 'Loan application submitted successfully.'}), 200

@app.route('/status/<loan_id>', methods=['GET'])
def get_loan_status(loan_id):
    # Search for the loan application with the given ID
    for loan_application in loan_applications:
        if loan_application.get('loan_id') == loan_id:
            return jsonify({'status': loan_application.get('status')}), 200

    # Loan application not found
    return jsonify({'error': 'Loan application not found.'}), 404

if __name__ == '__main__':
    app.run(debug=True)
```

This code sets up a Flask API with two routes. The `/apply` route accepts POST requests to submit a new loan application. The request data should contain the necessary information (personal details, income details, and employment details). The loan application is saved in an in-memory storage (list).

The `/status/<loan_id>` route accepts GET requests to retrieve the status of a loan application. The loan_id is used to search for the corresponding loan application in the storage. If found, the status is returned; otherwise, an error message is returned.

Please note that this is a simplified example and doesn't cover all the acceptance criteria. You would need to further develop and customize the code to meet all the requirements of your specific user story.