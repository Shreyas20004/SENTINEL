"""
Database initialization and session management
"""
import logging

from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, Session

from app.core.config import settings

logger = logging.getLogger(__name__)

Base = declarative_base()

# Async database engine
engine = create_async_engine(
    settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
    echo=settings.DATABASE_ECHO,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True
)

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db():
    """Get database session"""
    async with AsyncSessionLocal() as session:
        yield session


async def init_db():
    """Initialize database - create tables and enable PostGIS"""
    try:
        async with engine.begin() as conn:
            # Enable PostGIS
            await conn.exec(text("CREATE EXTENSION IF NOT EXISTS postgis"))
            logger.info("PostGIS extension enabled")
            
            # Create tables
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Database initialization error: {e}")
        raise


async def close_db():
    """Close database connection"""
    await engine.dispose()
