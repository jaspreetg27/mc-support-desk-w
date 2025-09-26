"""FastAPI dependencies."""

from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .core.redis_client import get_redis_client
from .db.session import get_db_session


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get database session dependency."""
    async with get_db_session() as session:
        yield session


async def get_redis():
    """Get Redis client dependency."""
    return await get_redis_client()
