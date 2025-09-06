import json
import pytest
from unittest.mock import Mock, patch

# Mock the entire ChatService module before importing lambda_function
mock_chat_service = Mock()
mock_chat_service.generate_response.return_value = {"response": "Mock response"}

with patch('creme_brulee_bot.services.chat_service.ChatService', return_value=mock_chat_service):
    from creme_brulee_bot.lambda_function import verify_signature, handle_command, lambda_handler

def test_verify_signature():
    """Test Discord signature verification"""
    event = {
        "headers": {
            "x-signature-ed25519": "valid_signature",
            "x-signature-timestamp": "timestamp"
        },
        "body": json.dumps({"type": 1})
    }
    
    # Should fail with invalid signature
    assert verify_signature(event) == False

def test_ping_request():
    """Test Discord PING handling"""
    event = {
        "headers": {
            "x-signature-ed25519": "signature",
            "x-signature-timestamp": "timestamp"
        },
        "body": json.dumps({"type": 1})
    }
    
    response = lambda_handler(event, None)
    assert response["statusCode"] == 200
    assert json.loads(response["body"])["type"] == 1

def test_chat_command():
    """Test chat command handling"""
    event = {
        "headers": {
            "x-signature-ed25519": "signature",
            "x-signature-timestamp": "timestamp"
        },
        "body": json.dumps({
            "type": 2,
            "data": {
                "name": "chat",
                "options": [{"value": "Hello"}]
            },
            "member": {"user": {"id": "123"}}
        })
    }
    
    # Mock verify_signature to return True
    with pytest.MonkeyPatch.context() as m:
        m.setattr("lambda_function.verify_signature", lambda x: True)
        response = lambda_handler(event, None)
        assert response["statusCode"] == 200 