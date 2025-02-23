import pytest
from ..discord_lambda import handle_interaction, verify_signature
import json

@pytest.mark.asyncio
async def test_chat_command():
    """Test basic chat command functionality"""
    test_body = {
        "type": 2,
        "data": {
            "name": "chat",
            "options": [
                {
                    "name": "message",
                    "value": "Hello, royal kitty!"
                }
            ]
        },
        "member": {
            "user": {
                "id": "test_user_123"
            }
        }
    }
    
    response = await handle_interaction(test_body)
    assert response["type"] == 4
    assert "content" in response["data"]

@pytest.mark.asyncio
async def test_decree_command():
    """Test decree command functionality"""
    test_body = {
        "type": 2,
        "data": {
            "name": "decree",
        },
        "member": {
            "user": {
                "id": "test_user_123"
            }
        }
    }
    
    response = await handle_interaction(test_body)
    assert response["type"] == 4
    assert "embeds" in response["data"]
    assert response["data"]["embeds"][0]["title"] == "🔰 Royal Decree 🔰"

@pytest.mark.asyncio
async def test_ping_command():
    """Test Discord ping verification"""
    test_body = {
        "type": 1  # PING
    }
    
    response = await handle_interaction(test_body)
    assert response["type"] == 1  # PONG

def test_signature_verification(mocker):
    """Test Discord signature verification"""
    # Mock a valid request
    valid_event = {
        "headers": {
            "x-signature-ed25519": "valid_signature",
            "x-signature-timestamp": "timestamp"
        },
        "body": json.dumps({"test": "data"})
    }
    
    # Mock VerifyKey verification
    mocker.patch('nacl.signing.VerifyKey.verify', return_value=True)
    assert verify_signature(valid_event) == True

    # Test invalid signature
    mocker.patch('nacl.signing.VerifyKey.verify', side_effect=Exception())
    assert verify_signature(valid_event) == False 