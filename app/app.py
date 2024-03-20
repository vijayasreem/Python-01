Here is a Python Flask API code that satisfies the given user story:

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

# Loan application form route
@app.route('/loan-application', methods=['POST'])
def loan_application():
    # Get loan application data from the request
    loan_application_data = request.json

    # Process loan application data
    # ...

    # Return a confirmation or acknowledgment of the loan application submission
    return jsonify({'message': 'Loan application submitted successfully.'}), 200

# Loan application status route
@app.route('/loan-application/status', methods=['GET'])
def loan_application_status():
    # Get loan application status data from the request
    application_id = request.args.get('application_id')

    # Get loan application status from the database
    # ...

    # Return loan application status
    return jsonify({'status': 'Approved'}), 200

if __name__ == '__main__':
    app.run(debug=True)
```

This code sets up two routes for the loan application process:

1. `/loan-application` - This route handles the submission of the loan application form. It expects a JSON payload containing the necessary information for the loan application. It processes the data and returns a confirmation or acknowledgment of the loan application submission.

2. `/loan-application/status` - This route allows the customer to track the status of their loan application. It expects an `application_id` as a query parameter and retrieves the application status from the database. It then returns the status of the loan application.

Please note that this is a basic implementation and will require further development and integration with a database and other necessary functionalities according to your specific requirements.