Here is an example of Python Flask API code that handles exceptions gracefully and provides informative error messages to the user:

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/transaction', methods=['POST'])
def transaction():
    try:
        # Perform transaction logic here
        
        # Return success response
        return jsonify({'message': 'Transaction successful'})

    except Exception as e:
        # Log the exception for later analysis
        app.logger.error(str(e))

        # Return error response with informative message
        return jsonify({'message': 'An error occurred during the transaction. Please try again later.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
```

In this code, we have a Flask route for the `/transaction` endpoint where the transaction logic is performed. Inside the `try` block, the transaction logic is executed. If any exception occurs during this process, it is caught in the `except` block.

Inside the `except` block, the exception is logged using Flask's logger (`app.logger.error`). This allows you to keep track of the exceptions for later analysis and improvement of system reliability.

A JSON response with an informative error message is returned to the user, indicating that an error occurred during the transaction and suggesting to try again later. The response has a status code of 500, which indicates a server-side error.

You can add more specific exception handling logic based on your application's requirements.