import pytest
from ..discord_lambda import lambda_handler
import json

@pytest.mark.asyncio
async def test_invalid_json():
    """Test handling of invalid JSON"""
    test_event = {
        "headers": {
            "x-signature-ed25519": "mock_signature",
            "x-signature-timestamp": "timestamp"
        },
        "body": "invalid json{"
    }
    
    response = await lambda_handler(test_event, None)
    assert response["statusCode"] == 500
    assert "error" in json.loads(response["body"])

@pytest.mark.asyncio
async def test_missing_required_fields():
    """Test handling of missing required fields"""
    test_event = {
        "headers": {
            "x-signature-ed25519": "mock_signature",
            "x-signature-timestamp": "timestamp"
        },
        "body": json.dumps({
            "type": 2,
            "data": {
                "name": "chat"
                # Missing options
            }
        })
    }
    
    with pytest.MonkeyPatch.context() as m:
        m.setattr("discord_lambda.verify_signature", lambda x: True)
        response = await lambda_handler(test_event, None)
        assert response["statusCode"] == 200
        response_data = json.loads(response["body"])
        assert "Meow? I don't understand that command." in response_data["data"]["content"]

@pytest.mark.asyncio
async def test_ai_service_error(mocker):
    """Test handling of AI service errors"""
    test_event = {
        "headers": {
            "x-signature-ed25519": "mock_signature",
            "x-signature-timestamp": "timestamp"
        },
        "body": json.dumps({
            "type": 2,
            "data": {
                "name": "chat",
                "options": [
                    {
                        "name": "message",
                        "value": "Hello!"
                    }
                ]
            },
            "member": {
                "user": {
                    "id": "test_user_123"
                }
            }
        })
    }
    
    # Mock AI service to raise an error
    mocker.patch(
        'services.chat_service.ChatService.generate_response',
        side_effect=Exception("AI service error")
    )
    
    with pytest.MonkeyPatch.context() as m:
        m.setattr("discord_lambda.verify_signature", lambda x: True)
        response = await lambda_handler(test_event, None)
        assert response["statusCode"] == 500 