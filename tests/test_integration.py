import pytest
from ..discord_lambda import lambda_handler
from ..services.chat_service import ChatService
from ..services.cache_service import CacheService

@pytest.mark.asyncio
async def test_full_chat_flow(mock_redis, mock_dynamo):
    """Test complete chat flow with caching and storage"""
    # First request
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
    
    # Mock signature verification
    with pytest.MonkeyPatch.context() as m:
        m.setattr("discord_lambda.verify_signature", lambda x: True)
        
        # First request should hit the AI
        response1 = await lambda_handler(test_event, None)
        assert response1["statusCode"] == 200
        
        # Same request should hit cache
        response2 = await lambda_handler(test_event, None)
        assert response2["statusCode"] == 200
        assert json.loads(response1["body"]) == json.loads(response2["body"])

@pytest.mark.asyncio
async def test_rate_limiting(mock_redis):
    """Test rate limiting functionality"""
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
                        "value": "Test message"
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
    
    with pytest.MonkeyPatch.context() as m:
        m.setattr("discord_lambda.verify_signature", lambda x: True)
        
        # Make multiple requests
        for _ in range(60):
            response = await lambda_handler(test_event, None)
            assert response["statusCode"] == 200
        
        # Next request should be rate limited
        response = await lambda_handler(test_event, None)
        assert response["statusCode"] == 429 