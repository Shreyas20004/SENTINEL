"""
SENTINEL Backend - Main FastAPI Application
Real-Time Public Safety AI System
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZIPMiddleware

from app.api import incidents, alerts, metrics, zones, cameras, dispatch, reports, websocket
from app.core.config import settings
from app.core.database import init_db
from app.core.redis_client import redis_client

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle manager"""
    # Startup
    logger.info("SENTINEL Backend starting...")
    await init_db()
    await redis_client.connect()
    logger.info("Database and Redis initialized")
    
    yield
    
    # Shutdown
    logger.info("SENTINEL Backend shutting down...")
    await redis_client.disconnect()
    logger.info("Cleanup complete")


# Initialize FastAPI application
app = FastAPI(
    title="SENTINEL API",
    description="Real-Time Public Safety AI System",
    version="1.0.0",
    lifespan=lifespan
)

# Middleware
app.add_middleware(GZIPMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "service": "SENTINEL"
    }


# Include routers
app.include_router(incidents.router, prefix="/api/v1", tags=["incidents"])
app.include_router(alerts.router, prefix="/api/v1", tags=["alerts"])
app.include_router(metrics.router, prefix="/api/v1", tags=["metrics"])
app.include_router(zones.router, prefix="/api/v1", tags=["zones"])
app.include_router(cameras.router, prefix="/api/v1", tags=["cameras"])
app.include_router(dispatch.router, prefix="/api/v1", tags=["dispatch"])
app.include_router(reports.router, prefix="/api/v1", tags=["reports"])
app.include_router(websocket.router, tags=["websocket"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "SENTINEL - Public Safety AI System",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
