import redis.asyncio as redis
from app.core.config import settings
from typing import Optional, Any
import json
from loguru import logger


class RedisClient:
    """Redis client wrapper"""
    
    def __init__(self, url: str):
        self.redis = redis.from_url(url, encoding="utf-8", decode_responses=True)
    
    async def get(self, key: str) -> Optional[str]:
        """Get value by key"""
        try:
            return await self.redis.get(key)
        except Exception as e:
            logger.error(f"Redis GET error for key {key}: {e}")
            return None
    
    async def set(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        """Set key-value pair with optional expiration"""
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            result = await self.redis.set(key, value, ex=expire)
            return bool(result)
        except Exception as e:
            logger.error(f"Redis SET error for key {key}: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete key"""
        try:
            result = await self.redis.delete(key)
            return bool(result)
        except Exception as e:
            logger.error(f"Redis DELETE error for key {key}: {e}")
            return False
    
    async def incr(self, key: str, amount: int = 1) -> Optional[int]:
        """Increment key value"""
        try:
            return await self.redis.incr(key, amount)
        except Exception as e:
            logger.error(f"Redis INCR error for key {key}: {e}")
            return None
    
    async def expire(self, key: str, seconds: int) -> bool:
        """Set key expiration"""
        try:
            return await self.redis.expire(key, seconds)
        except Exception as e:
            logger.error(f"Redis EXPIRE error for key {key}: {e}")
            return False
    
    async def ping(self) -> bool:
        """Test Redis connection"""
        try:
            await self.redis.ping()
            return True
        except Exception as e:
            logger.error(f"Redis PING error: {e}")
            return False
    
    async def close(self):
        """Close Redis connection"""
        await self.redis.close()


redis_client = RedisClient(settings.redis_url)