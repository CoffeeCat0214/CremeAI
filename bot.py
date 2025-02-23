import discord
from discord import app_commands
from services.chat_service import ChatService
import os
from dotenv import load_dotenv
import logging
import json
from nacl.signing import VerifyKey
import asyncio

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('discord')

load_dotenv()

class CremeBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.presences = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.chat_service = ChatService()

    async def setup_hook(self):
        await self.tree.sync()
        
    async def on_ready(self):
        logger.info(f'Logged in as {self.user} (ID: {self.user.id})')
        logger.info('------')

async def handle_interaction(body, client):
    """Handle Discord interaction"""
    try:
        if body['type'] == 2:  # APPLICATION_COMMAND
            command_name = body['data']['name']
            if command_name == 'chat':
                message = body['data']['options'][0]['value']
                response = await client.chat_service.generate_response(
                    user_id=body['member']['user']['id'],
                    message=message
                )
            elif command_name == 'decree':
                response = await client.chat_service.generate_response(
                    user_id=body['member']['user']['id'],
                    message="Issue a royal decree!"
                )
            
            return {
                'type': 4,
                'data': {
                    'content': response['response']
                }
            }
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {
            'type': 4,
            'data': {
                'content': "Meow? Something went wrong!"
            }
        }

def verify_signature(event):
    """Verify that the request came from Discord"""
    try:
        public_key = os.getenv('DISCORD_PUBLIC_KEY')
        signature = event['headers']['x-signature-ed25519']
        timestamp = event['headers']['x-signature-timestamp']
        body = event['body']

        verify_key = VerifyKey(bytes.fromhex(public_key))
        verify_key.verify(f"{timestamp}{body}".encode(), bytes.fromhex(signature))
        return True
    except Exception as e:
        logger.error(f"Signature verification failed: {str(e)}")
        return False

def lambda_handler(event, context):
    """AWS Lambda handler"""
    logger.info(f"Received event: {json.dumps(event)}")
    
    # Verify the request
    if not verify_signature(event):
        return {
            'statusCode': 401,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'invalid request signature'})
        }

    # Parse the request body
    body = json.loads(event['body'])
    
    # Handle Discord's ping
    if body['type'] == 1:  # PING
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'type': 1})  # PONG
        }

    # For now, just acknowledge other interactions
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({
            'type': 1
        })
    }

def run_bot():
    client.run(os.getenv('DISCORD_BOT_TOKEN'))

if __name__ == "__main__":
    run_bot() 