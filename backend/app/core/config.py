"""
Configuration management for SENTINEL backend
"""
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "SENTINEL"
    DESCRIPTION: str = "Real-Time Public Safety AI System"
    VERSION: str = "1.0.0"
    
    # Server
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 4
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000", "http://localhost:8000"]
    
    # Database
    DATABASE_URL: str = "postgresql://sentinel:sentinel_secure_pwd_2024@localhost:5432/sentinel_db"
    DATABASE_ECHO: bool = False
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_CACHE_TTL: int = 300  # 5 minutes
    
    # JWT
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    
    # AI/ML
    YOLO_MODEL_PATH: str = "models/yolov8n.pt"
    CONFIDENCE_THRESHOLD: float = 0.5
    IOU_THRESHOLD: float = 0.45
    
    # Detection Rules
    LOITERING_THRESHOLD_SECONDS: int = 600  # 10 minutes
    ABANDONED_OBJECT_THRESHOLD_SECONDS: int = 300  # 5 minutes
    CROWD_SURGE_THRESHOLD: int = 10  # persons per zone
    
    # Inference
    INFERENCE_BATCH_SIZE: int = 4
    INFERENCE_TIMEOUT_MS: int = 50
    GPU_ENABLED: bool = True
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Metrics
    METRICS_WINDOW_SIZE: int = 3600  # 1 hour
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
