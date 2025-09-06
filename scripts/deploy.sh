#!/bin/bash

# Register Discord commands
echo "Registering Discord commands..."
python scripts/register_commands.py

# Deploy to AWS Lambda
echo "Deploying to AWS Lambda..."
serverless deploy

# Output the endpoint URL
echo "Deployment complete! Use the following URL as your Discord Interactions Endpoint:"
serverless info --verbose | grep "POST - /api/interactions" 
