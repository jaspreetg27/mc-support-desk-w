"""Health check router."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from ..deps import get_db, get_redis
from ..logging import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/healthz")
async def healthz(
    db: AsyncSession = Depends(get_db),
    redis = Depends(get_redis),
):
    """Health check endpoint with database and Redis connectivity."""
    health_status = {
        "status": "ok",
        "checks": {
            "database": "unknown",
            "redis": "unknown",
        }
    }
    
    # Check database connectivity
    try:
        result = await db.execute(text("SELECT 1"))
        result.scalar()
        health_status["checks"]["database"] = "ok"
    except Exception as e:
        logger.error("Database health check failed", error=str(e))
        health_status["checks"]["database"] = "error"
        health_status["status"] = "error"
    
    # Check Redis connectivity
    try:
        await redis.ping()
        health_status["checks"]["redis"] = "ok"
    except Exception as e:
        logger.error("Redis health check failed", error=str(e))
        health_status["checks"]["redis"] = "error"
        health_status["status"] = "error"
    
    if health_status["status"] == "error":
        raise HTTPException(status_code=503, detail=health_status)
    
    return health_status
