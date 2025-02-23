import redis
import json
import hashlib
from typing import Any, Optional
from ..config import get_settings

settings = get_settings()

class CacheService:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            decode_responses=True
        )
        self.default_ttl = 3600  # 1 hour

    def _generate_key(self, prefix: str, data: dict) -> str:
        """Generate a unique cache key based on input data"""
        data_str = json.dumps(data, sort_keys=True)
        return f"{prefix}:{hashlib.md5(data_str.encode()).hexdigest()}"

    async def get_cached_response(self, user_id: str, message: str, platform: str) -> Optional[dict]:
        """Get cached chat response"""
        cache_key = self._generate_key("chat", {
            "user_id": user_id,
            "message": message,
            "platform": platform
        })
        
        cached = self.redis_client.get(cache_key)
        return json.loads(cached) if cached else None

    async def cache_response(self, user_id: str, message: str, platform: str, response: dict, ttl: int = None):
        """Cache a chat response"""
        cache_key = self._generate_key("chat", {
            "user_id": user_id,
            "message": message,
            "platform": platform
        })
        
        self.redis_client.setex(
            cache_key,
            ttl or self.default_ttl,
            json.dumps(response)
        )

    async def invalidate_cache(self, pattern: str = None):
        """Invalidate cache entries matching pattern"""
        if pattern:
            keys = self.redis_client.keys(f"*{pattern}*")
            if keys:
                self.redis_client.delete(*keys) 