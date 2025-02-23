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
    chat_service = ChatService()
    
    if body["type"] == 1:  # PING
        return {"type": 1}  # PONG
        
    if body["type"] == 2:  # APPLICATION_COMMAND
        response = await chat_service.generate_response(
            user_id=body["member"]["user"]["id"],
            message=body["data"]["options"][0]["value"],
            platform="discord"
        )
        
        return {
            "type": 4,
            "data": {
                "content": response["response"]
            }
        }

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """AWS Lambda entry point"""
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