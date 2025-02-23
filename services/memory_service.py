import redis
import json
import boto3
from typing import List, Dict
import os
import time

class MemoryService:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            decode_responses=True
        )
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(os.getenv("DYNAMODB_TABLE"))

    async def get_chat_history(self, user_id: str) -> List[Dict[str, str]]:
        # First check Redis for recent history
        recent_history = self.redis_client.lrange(f"chat_history:{user_id}", 0, -1)
        
        if recent_history:
            return [json.loads(msg) for msg in recent_history]

        # If not in Redis, check DynamoDB
        response = self.table.query(
            KeyConditionExpression='user_id = :uid',
            ExpressionAttributeValues={':uid': user_id},
            Limit=10,
            ScanIndexForward=False
        )

        history = []
        for item in response['Items']:
            history.append({
                "role": "user" if item['is_user'] else "assistant",
                "content": item['message']
            })

        return history

    async def store_interaction(
        self, 
        user_id: str, 
        message: str, 
        response: str, 
        platform: str
    ):
        # Store in Redis for short-term memory
        chat_key = f"chat_history:{user_id}"
        
        self.redis_client.lpush(
            chat_key,
            json.dumps({"role": "user", "content": message})
        )
        self.redis_client.lpush(
            chat_key,
            json.dumps({"role": "assistant", "content": response})
        )
        
        # Trim to last 10 messages
        self.redis_client.ltrim(chat_key, 0, 9)

        # Store in DynamoDB for long-term memory
        self.table.put_item(Item={
            'user_id': user_id,
            'timestamp': int(time.time()),
            'message': message,
            'response': response,
            'platform': platform
        }) 