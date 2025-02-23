from fastapi import Request, HTTPException
import redis
import time
from typing import Optional
from ..config import get_settings

settings = get_settings()

class RateLimiter:
    def __init__(self):
        self.rate_limits = {}
        self.window_size = 60  # 1 minute
        self.max_requests = 60  # 60 requests per minute

    async def check_rate_limit(self, user_id: str) -> bool:
        now = time.time()
        if user_id not in self.rate_limits:
            self.rate_limits[user_id] = []
        
        # Clean old requests
        self.rate_limits[user_id] = [
            t for t in self.rate_limits[user_id] 
            if t > now - self.window_size
        ]
        
        if len(self.rate_limits[user_id]) >= self.max_requests:
            return False
            
        self.rate_limits[user_id].append(now)
        return True 