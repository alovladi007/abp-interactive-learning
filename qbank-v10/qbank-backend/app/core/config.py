import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field, SecretStr, PostgresDsn, RedisDsn

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "QBank API"
    APP_VERSION: str = "10.0.0"
    DEBUG: bool = Field(default=False)
    ENVIRONMENT: str = Field(default="development")
    API_V1_PREFIX: str = "/v1"
    
    # Security
    SECRET_KEY: SecretStr = Field(default="change-me-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    CORS_ORIGINS: List[str] = ["*"]
    
    # Database
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://qbank:qbank@localhost:5432/qbank"
    )
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 40
    DATABASE_POOL_TIMEOUT: int = 30
    
    # Redis
    REDIS_URL: str = Field(default="redis://localhost:6379/0")
    REDIS_POOL_SIZE: int = 50
    REDIS_DECODE_RESPONSES: bool = True
    CACHE_TTL: int = 3600  # 1 hour
    
    # Kafka
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_TOPIC_EVENTS: str = "events.qbank"
    KAFKA_TOPIC_ANALYTICS: str = "analytics.qbank"
    KAFKA_CONSUMER_GROUP: str = "qbank-backend"
    
    # Elasticsearch
    ELASTICSEARCH_URL: str = "http://localhost:9200"
    ELASTICSEARCH_INDEX_QUESTIONS: str = "qbank-questions"
    ELASTICSEARCH_INDEX_ANALYTICS: str = "qbank-analytics"
    
    # ClickHouse
    CLICKHOUSE_URL: str = "clickhouse://localhost:9000/qbank"
    
    # Multi-tenancy
    TENANT_ID: str = Field(default="00000000-0000-0000-0000-000000000001")
    ENABLE_MULTI_TENANCY: bool = True
    
    # Queue/Worker
    RQ_QUEUE: str = "calibration"
    RQ_WORKER_CONCURRENCY: int = 4
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"
    
    # Exposure Control
    MAX_DAILY_EXPOSURES: int = 500
    EXPOSURE_CONTROL_ENABLED: bool = True
    DEFAULT_SH_P: float = 1.0
    
    # IRT Settings
    IRT_MODEL: str = "3PL"  # 2PL or 3PL
    IRT_MIN_RESPONSES: int = 200
    ADAPTIVE_ENABLED: bool = True
    
    # ML Models
    EMBEDDINGS_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    DIFFICULTY_PREDICTION_ENABLED: bool = True
    
    # Observability
    ENABLE_METRICS: bool = True
    ENABLE_TRACING: bool = True
    JAEGER_AGENT_HOST: str = "localhost"
    JAEGER_AGENT_PORT: int = 6831
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    
    # Feature Flags
    FEATURE_SEMANTIC_SEARCH: bool = True
    FEATURE_RECOMMENDATIONS: bool = True
    FEATURE_BULK_IMPORT: bool = True
    FEATURE_ADVANCED_ANALYTICS: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()