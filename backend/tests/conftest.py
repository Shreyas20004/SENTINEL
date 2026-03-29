"""
Shared pytest fixtures and configuration
"""

import pytest
import asyncio
import os
from typing import AsyncGenerator

# Set test environment variables
os.environ["DATABASE_URL"] = "postgresql+asyncpg://test:test@localhost/sentinel_test"
os.environ["REDIS_URL"] = "redis://localhost:6379/1"
os.environ["ENV"] = "test"


def pytest_configure(config):
    """Pytest configuration hook"""
    config.addinivalue_line(
        "markers", "asyncio: mark test as async"
    )


@pytest.fixture(scope="session")
def event_loop():
    """Event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def async_client():
    """Async HTTP client for testing API"""
    from httpx import AsyncClient
    from app.main import app
    
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client


@pytest.fixture
async def db_session():
    """Test database session"""
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy.orm import sessionmaker
    
    # Use test database
    engine = create_async_engine(
        os.environ["DATABASE_URL"],
        echo=False
    )
    
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    # Create tables
    async with engine.begin() as conn:
        from app.models import Base
        await conn.run_sync(Base.metadata.create_all)
    
    async with async_session() as session:
        yield session
    
    # Clean up
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()


@pytest.fixture
async def redis_client():
    """Test Redis client"""
    import redis.asyncio as redis
    
    client = redis.from_url(os.environ["REDIS_URL"])
    
    # Flush test database
    await client.flushdb()
    
    yield client
    
    # Cleanup
    await client.flushdb()
    await client.close()


@pytest.fixture
def sample_incident_data():
    """Sample incident data"""
    return {
        "incident_type": "LOITERING",
        "severity": "HIGH",
        "zone_id": "zone_1",
        "description": "Test incident",
        "location": {
            "type": "Point",
            "coordinates": [28.6139, 77.2090]
        }
    }


@pytest.fixture
def sample_alert_data():
    """Sample alert data"""
    return {
        "incident_id": "incident_1",
        "camera_id": "camera_1",
        "alert_type": "MOTION",
        "severity": "MEDIUM",
        "confidence": 0.95
    }


@pytest.fixture
def sample_camera_data():
    """Sample camera data"""
    return {
        "name": "Main Gate",
        "zone_id": "zone_1",
        "rtsp_url": "rtsp://example.com/stream",
        "is_active": True
    }


@pytest.fixture
def sample_zone_data():
    """Sample zone data"""
    return {
        "name": "Zone A",
        "description": "Main entrance",
        "polygon": {
            "type": "Polygon",
            "coordinates": [[
                [77.2, 28.6],
                [77.3, 28.6],
                [77.3, 28.7],
                [77.2, 28.7],
                [77.2, 28.6]
            ]]
        }
    }
