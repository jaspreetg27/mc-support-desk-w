"""Redis client configuration."""

import redis.asyncio as redis

from ..config import settings
from ..logging import get_logger

logger = get_logger(__name__)

# Global Redis client instance
_redis_client: redis.Redis = None


async def get_redis_client() -> redis.Redis:
    """Get Redis client instance."""
    global _redis_client
    
    if _redis_client is None:
        _redis_client = redis.from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5,
            retry_on_timeout=True,
        )
        logger.info("Redis client initialized", redis_url=settings.redis_url)
    
    return _redis_client


async def close_redis_client() -> None:
    """Close Redis client connection."""
    global _redis_client
    
    if _redis_client:
        await _redis_client.close()
        _redis_client = None
        logger.info("Redis client closed")
