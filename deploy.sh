#!/bin/bash

# Build deployment package
pip install -r requirements.txt --target ./package
cd package
zip -r ../deployment.zip .
cd ..
zip -g deployment.zip *.py services/*.py

# Deploy to AWS Lambda
aws lambda update-function-code \
    --function-name creme-brulee-chatbot \
    --zip-file fileb://deployment.zip

# Clean up
rm -rf package
rm deployment.zip 