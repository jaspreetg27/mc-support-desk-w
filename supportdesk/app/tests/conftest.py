"""Test configuration and fixtures."""

import uuid
from collections.abc import AsyncIterator, Iterator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import StaticPool

from ..db.base import Base
from ..main import app
from ..deps import get_db  # normal app dependency

# In-memory SQLite for tests
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# One shared engine/connection pool for all tests
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Make the app use the SQLite test DB instead of Postgres
async def override_get_db() -> AsyncIterator[AsyncSession]:
    async with AsyncSession(test_engine) as session:
        yield session

app.dependency_overrides[get_db] = override_get_db


@pytest_asyncio.fixture(autouse=True)
async def _create_drop_schema() -> AsyncIterator[None]:
    """Create all tables before each test, drop after."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield
    finally:
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session() -> AsyncIterator[AsyncSession]:
    """Provide a raw DB session if a test needs it."""
    async with AsyncSession(test_engine) as session:
        yield session


@pytest.fixture
def client() -> Iterator[TestClient]:
    """Sync test client."""
    with TestClient(app) as c:
        yield c


@pytest_asyncio.fixture
async def async_client() -> AsyncIterator[AsyncClient]:
    """Async test client."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def sample_tenant_data():
    return {"id": uuid.uuid4(), "name": "Test Tenant"}


@pytest.fixture
def sample_customer_data():
    return {
        "id": uuid.uuid4(),
        "tenant_id": uuid.uuid4(),
        "platform": "wa",
        "platform_user_id": "1234567890",
        "phone": "+1234567890",
        "email": "test@example.com",
    }
