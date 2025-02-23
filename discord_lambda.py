import json
import hmac
import hashlib
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from typing import Dict, Any
import asyncio
from mangum import Mangum

from services.chat_service import ChatService
from config import get_settings

settings = get_settings()

def verify_signature(event: Dict[str, Any]) -> bool:
    """Verify Discord interaction signature"""
    try:
        body = event.get('body', '')
        auth_sig = event['headers'].get('x-signature-ed25519')
        auth_ts = event['headers'].get('x-signature-timestamp')
        
        verify_key = VerifyKey(bytes.fromhex(settings.DISCORD_PUBLIC_KEY))
        verify_key.verify(
            f"{auth_ts}{body}".encode(),
            bytes.fromhex(auth_sig)
        )
        return True
    except (BadSignatureError, Exception):
        return False

async def handle_interaction(body: Dict[str, Any]) -> Dict[str, Any]:
    """Handle Discord interaction"""
    interaction_type = body.get('type', 0)
    
    # Ping
    if interaction_type == 1:
        return {
            "type": 1  # PONG
        }
    
    # Application Command
    if interaction_type == 2:
        command_name = body.get('data', {}).get('name', '')
        
        if command_name == "chat":
            # Get the message content
            options = body.get('data', {}).get('options', [])
            message = next((opt['value'] for opt in options if opt['name'] == 'message'), '')
            
            # Generate response
            chat_service = ChatService()
            response = await chat_service.generate_response(
                user_id=str(body['member']['user']['id']),
                message=message,
                platform='discord'
            )
            
            return {
                "type": 4,  # CHANNEL_MESSAGE_WITH_SOURCE
                "data": {
                    "content": response['response'],
                    "embeds": [
                        {
                            "title": "🔰 Royal Decree 🔰",
                            "description": response['decree'],
                            "color": 0xFFD700
                        }
                    ] if response.get('decree') else []
                }
            }
        
        elif command_name == "decree":
            chat_service = ChatService()
            response = await chat_service.generate_response(
                user_id=str(body['member']['user']['id']),
                message="I demand a royal decree!",
                platform='discord'
            )
            
            return {
                "type": 4,
                "data": {
                    "embeds": [
                        {
                            "title": "🔰 Royal Decree 🔰",
                            "description": response.get('decree', 'No decree at this time'),
                            "color": 0xFFD700
                        }
                    ]
                }
            }
    
    return {
        "type": 4,
        "data": {
            "content": "Meow? I don't understand that command."
        }
    }

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """AWS Lambda handler for Discord interactions"""
    try:
        # Verify signature
        if not verify_signature(event):
            return {
                'statusCode': 401,
                'body': json.dumps({'error': 'Invalid signature'})
            }
        
        # Parse body
        body = json.loads(event['body'])
        
        # Handle interaction using asyncio
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(handle_interaction(body))
        
        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        } 