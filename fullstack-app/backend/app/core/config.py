"""
Application configuration settings
"""
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Neural Machine Translation API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "English to Tamil Neural Machine Translation using Transformers"
    
    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    RELOAD: bool = False
    
    # CORS Settings
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",  # Next.js dev server
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "https://your-frontend-domain.com"  # Production frontend
    ]
    
    # Model Settings
    MODEL_PATH: str = "./saved_model"
    MAX_INPUT_LENGTH: int = 512
    MAX_OUTPUT_LENGTH: int = 512
    DEFAULT_NUM_BEAMS: int = 4
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Redis Settings (optional)
    REDIS_URL: Optional[str] = None
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Logging
    LOG_LEVEL: str = "INFO"


# Global settings instance
settings = Settings()
