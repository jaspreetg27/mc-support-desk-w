"""Test configuration and fixtures."""

import asyncio
import uuid
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import StaticPool

from ..db.base import Base
from ..db.session import AsyncSessionLocal
from ..main import app


# Test database URL (in-memory SQLite for tests)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create test engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create test database session."""
    # Create tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create session
    async with AsyncSession(test_engine) as session:
        yield session
    
    # Drop tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """Create test client."""
    with TestClient(app) as c:
        yield c


@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None, None]:
    """Create async test client."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def sample_tenant_data():
    """Sample tenant data for tests."""
    return {
        "id": uuid.uuid4(),
        "name": "Test Tenant",
    }


@pytest.fixture
def sample_customer_data():
    """Sample customer data for tests."""
    return {
        "id": uuid.uuid4(),
        "tenant_id": uuid.uuid4(),
        "platform": "wa",
        "platform_user_id": "1234567890",
        "phone": "+1234567890",
        "email": "test@example.com",
    }
