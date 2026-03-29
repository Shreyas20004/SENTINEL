"""
Redis client for real-time alert streaming and caching
"""
import json
import logging
from typing import Any, Optional

import redis.asyncio as redis
from redis.asyncio import Redis

from app.core.config import settings

logger = logging.getLogger(__name__)


class RedisClient:
    """Redis client wrapper"""
    
    def __init__(self, url: str):
        self.url = url
        self.client: Optional[Redis] = None
    
    async def connect(self):
        """Connect to Redis"""
        try:
            self.client = await redis.from_url(
                self.url,
                encoding="utf8",
                decode_responses=True,
                socket_connect_timeout=5,
                socket_keepalive=True
            )
            await self.client.ping()
            logger.info("Connected to Redis")
        except Exception as e:
            logger.error(f"Redis connection error: {e}")
            raise
    
    async def disconnect(self):
        """Disconnect from Redis"""
        if self.client:
            await self.client.close()
            logger.info("Disconnected from Redis")
    
    async def publish(self, channel: str, message: dict):
        """Publish message to channel"""
        if not self.client:
            logger.warning("Redis client not connected")
            return
        
        try:
            await self.client.publish(channel, json.dumps(message))
        except Exception as e:
            logger.error(f"Redis publish error: {e}")
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not self.client:
            return None
        
        try:
            value = await self.client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Redis get error: {e}")
            return None
    
    async def set(self, key: str, value: Any, ttl: int = 300):
        """Set value in cache"""
        if not self.client:
            return
        
        try:
            await self.client.setex(
                key,
                ttl,
                json.dumps(value, default=str)
            )
        except Exception as e:
            logger.error(f"Redis set error: {e}")
    
    async def delete(self, key: str):
        """Delete value from cache"""
        if not self.client:
            return
        
        try:
            await self.client.delete(key)
        except Exception as e:
            logger.error(f"Redis delete error: {e}")


# Global Redis client instance
redis_client = RedisClient(settings.REDIS_URL)
