from mangum import Mangum
from main import app
import os
import json

# Create Mangum handler for AWS Lambda
handler = Mangum(app)

# Add custom exception handling for Lambda
def lambda_handler(event, context):
    try:
        response = handler(event, context)
        return response
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            }),
            "headers": {
                "Content-Type": "application/json"
            }
        } 