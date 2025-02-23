from fastapi import Request, HTTPException
import redis
import time
from typing import Optional
from ..config import get_settings

settings = get_settings()

class RateLimiter:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            decode_responses=True
        )
        self.rate_limit = 60  # requests per minute
        self.window = 60  # seconds

    async def check_rate_limit(self, request: Request):
        client_ip = request.client.host
        user_id = request.headers.get("X-User-ID")
        
        # Create unique key for user/IP
        key = f"rate_limit:{user_id or client_ip}"
        
        current = int(time.time())
        window_start = current - self.window
        
        # Remove old requests
        self.redis_client.zremrangebyscore(key, 0, window_start)
        
        # Count requests in current window
        request_count = self.redis_client.zcard(key)
        
        if request_count >= self.rate_limit:
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Please try again later."
            )
        
        # Add current request
        self.redis_client.zadd(key, {str(current): current})
        # Set expiry
        self.redis_client.expire(key, self.window) 