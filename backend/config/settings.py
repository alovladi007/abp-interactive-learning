from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "ABP Video Generation API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    API_PREFIX: str = "/api/v1"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 4
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost/abp_video"
    REDIS_URL: str = "redis://localhost:6379"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # AI Services
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    REPLICATE_API_TOKEN: Optional[str] = None
    ELEVEN_API_KEY: Optional[str] = None
    SUNO_API_KEY: Optional[str] = None
    
    # Cloud Storage
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "us-east-1"
    S3_BUCKET: str = "abp-videos"
    
    # Cloudflare R2
    R2_ACCOUNT_ID: Optional[str] = None
    R2_ACCESS_KEY_ID: Optional[str] = None
    R2_SECRET_ACCESS_KEY: Optional[str] = None
    R2_BUCKET: str = "abp-videos"
    
    # Stripe
    STRIPE_SECRET_KEY: Optional[str] = None
    STRIPE_WEBHOOK_SECRET: Optional[str] = None
    STRIPE_PRICE_ID: str = "price_generation_credit"
    
    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    # Video Processing
    MAX_VIDEO_DURATION: int = 60  # seconds
    DEFAULT_FPS: int = 24
    DEFAULT_RESOLUTION: str = "1920x1080"
    UPSCALE_FACTOR: int = 2
    INTERPOLATION_FACTOR: int = 2
    
    # Paths
    TEMP_DIR: str = "/tmp/abp-video"
    RIFE_BIN: str = "/opt/rife/rife-ncnn-vulkan"
    ESRGAN_BIN: str = "/opt/realesrgan/realesrgan-ncnn-vulkan"
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 10
    RATE_LIMIT_PER_HOUR: int = 100
    
    # Monitoring
    SENTRY_DSN: Optional[str] = None

    # Medical AI - Neo4j Knowledge Graph
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "password"

    # Medical Data Integration
    MEDICAL_DATA_UPLOAD_DIR: str = "/tmp/medical-data-uploads"
    MEDICAL_DATA_TEMP_DIR: str = "/tmp/medical-data-temp"
    INTEGRATION_BATCH_SIZE: int = 1000
    MAX_CONCURRENT_INTEGRATIONS: int = 3
    CLEANUP_OLD_JOBS_DAYS: int = 7

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()