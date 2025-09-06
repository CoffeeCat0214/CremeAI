import json
from lambda_function import lambda_handler

# Load test event
with open('test_event.json', 'r') as f:
    test_event = json.load(f)

# Run handler
response = lambda_handler(test_event, None)
print(json.dumps(response, indent=2)) 