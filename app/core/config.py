#No AI assistance was used for creating this file
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings and configuration."""
    
    # Application metadata
    PROJECT_NAME: str = "AI Semantic Code Refactorer"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database configuration
    DATABASE_URL: str = "postgresql://postgres:6865@localhost:5432/code_refactorer"

    # Security settings
    SECRET_KEY: str = "secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # OpenAI API configuration
    OPENAI_API_KEY: str = "openai-api-key"

    # Frontend configuration
    FRONTEND_URL: str = "http://localhost:3000"

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 