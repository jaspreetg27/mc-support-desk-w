"""Main FastAPI application."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from .logging import configure_logging, get_logger
from .routers.customers import router as customers_router
from .routers.health import router as health_router
from .routers.tenants import router as tenants_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    configure_logging()
    logger = get_logger(__name__)
    logger.info("Starting SupportDesk API")
    
    yield
    
    # Shutdown
    logger.info("Shutting down SupportDesk API")


app = FastAPI(
    title="Multi-Channel Support Desk AI",
    description="Production-grade backend for multi-channel customer support",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "supportdesk",
        "status": "ok",
        "version": "0.1.0",
    }


# Include routers
app.include_router(health_router)
app.include_router(tenants_router)
app.include_router(customers_router)
