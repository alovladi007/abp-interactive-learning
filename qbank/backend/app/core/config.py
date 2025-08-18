"""
Configuration settings for QBank system
"""

from typing import List, Union
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, field_validator
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Advanced QBank System"
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://qbank_user:qbank_secure_pass_2024@localhost:5432/qbank"
    )
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "qbank-secret-key-2024-secure")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # IRT Model Settings
    IRT_MODEL: str = os.getenv("IRT_MODEL", "3PL")  # 1PL, 2PL, or 3PL
    
    # Sympson-Hetter Exposure Control
    EXPOSURE_RATE_MAX: float = float(os.getenv("EXPOSURE_RATE_MAX", "0.25"))
    EXPOSURE_CONTROL_ENABLED: bool = True
    
    # Calibration Settings
    MIN_RESPONSES_FOR_CALIBRATION: int = int(
        os.getenv("MIN_RESPONSES_FOR_CALIBRATION", "30")
    )
    CALIBRATION_METHOD: str = "MMLE"  # Maximum Marginal Likelihood Estimation
    CALIBRATION_INTERVAL_HOURS: int = 24
    
    # Adaptive Testing Settings
    INITIAL_ABILITY_ESTIMATE: float = 0.0
    MIN_ITEMS_FOR_ESTIMATE: int = 5
    MAX_ITEMS_PER_TEST: int = 50
    STOPPING_CRITERION_SE: float = 0.3  # Standard error threshold
    
    # Question Pool Settings
    MIN_POOL_SIZE: int = 100
    MAX_POOL_SIZE: int = 10000
    CONTENT_BALANCING_ENABLED: bool = True
    
    # Performance Settings
    CACHE_TTL_SECONDS: int = 3600
    MAX_CONCURRENT_SESSIONS: int = 10000
    SESSION_TIMEOUT_MINUTES: int = 180
    
    # Analytics Settings
    ANALYTICS_ENABLED: bool = True
    ANALYTICS_RETENTION_DAYS: int = 365
    
    # Monitoring
    SENTRY_DSN: str = os.getenv("SENTRY_DSN", "")
    PROMETHEUS_ENABLED: bool = True
    
    # Testing
    TESTING: bool = os.getenv("TESTING", "False").lower() == "true"
    
    class Config:
        case_sensitive = True
        env_file = ".env"

# Create settings instance
settings = Settings()

# IRT Model Parameters
IRT_PARAMETERS = {
    "1PL": {
        "discrimination": 1.0,  # Fixed discrimination
        "guessing": 0.0,  # No guessing parameter
        "name": "Rasch Model"
    },
    "2PL": {
        "discrimination": "variable",  # Variable discrimination
        "guessing": 0.0,  # No guessing parameter
        "name": "Two-Parameter Logistic"
    },
    "3PL": {
        "discrimination": "variable",  # Variable discrimination
        "guessing": "variable",  # Variable guessing parameter
        "name": "Three-Parameter Logistic"
    }
}

# Sympson-Hetter Parameters
SYMPSON_HETTER_CONFIG = {
    "alpha": 0.05,  # Significance level
    "beta": 0.20,  # Type II error rate
    "k": 0.25,  # Target exposure rate
    "method": "conditional",  # conditional or unconditional
    "fade_rate": 0.999,  # Exposure probability fade rate
    "min_exposure": 0.01,  # Minimum exposure probability
    "max_exposure": 0.30,  # Maximum exposure probability
}

# Content Specifications
CONTENT_SPECS = {
    "mathematics": {
        "algebra": 0.30,
        "geometry": 0.25,
        "calculus": 0.25,
        "statistics": 0.20
    },
    "science": {
        "physics": 0.25,
        "chemistry": 0.25,
        "biology": 0.25,
        "earth_science": 0.25
    },
    "english": {
        "reading": 0.35,
        "writing": 0.35,
        "grammar": 0.30
    }
}

# Difficulty Levels
DIFFICULTY_LEVELS = {
    "very_easy": (-3.0, -2.0),
    "easy": (-2.0, -1.0),
    "medium": (-1.0, 1.0),
    "hard": (1.0, 2.0),
    "very_hard": (2.0, 3.0)
}

# Response Time Parameters
RESPONSE_TIME_CONFIG = {
    "model": "lognormal",  # lognormal or exponential
    "min_time": 10,  # Minimum response time in seconds
    "max_time": 300,  # Maximum response time in seconds
    "outlier_threshold": 3.0,  # Standard deviations for outlier detection
}