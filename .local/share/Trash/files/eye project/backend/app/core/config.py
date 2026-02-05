from pydantic_settings import BaseSettings
from typing import List, Optional
import os


class Settings(BaseSettings):
    # App settings
    APP_NAME: str = "Eye Disease Detection API"
    DEBUG: bool = False
    VERSION: str = "1.0.0"
    
    # Database settings
    DATABASE_URL: str = "postgresql://user:password@localhost/eyedisease"
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    
    # Security settings
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS settings
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "https://yourdomain.com"
    ]
    
    # ML Model settings
    MODEL_PATH: str = "ml/models/weights/best_model.pth"
    MODEL_CONFIDENCE_THRESHOLD: float = 0.7
    MAX_IMAGE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_IMAGE_TYPES: List[str] = ["image/jpeg", "image/png", "image/webp"]
    
    # Redis settings
    REDIS_URL: str = "redis://localhost:6379"
    
    # Celery settings
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    # File upload settings
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # Monitoring settings
    SENTRY_DSN: Optional[str] = None
    LOG_LEVEL: str = "INFO"
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    
    # Medical disclaimer
    MEDICAL_DISCLAIMER: str = """
    This application is for educational and screening purposes only and is NOT a 
    replacement for professional medical diagnosis. Always consult with qualified 
    healthcare professionals for medical decisions.
    """
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()