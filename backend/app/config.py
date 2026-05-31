"""
Configuration Management
Centralized configuration using Pydantic Settings for type safety and validation
"""

from pydantic_settings import BaseSettings
from pydantic import Field, validator
from typing import List
import os
from pathlib import Path


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    Provides type validation and default values
    """
    
    # Application
    APP_NAME: str = Field(default="AI Resume Interview System")
    APP_VERSION: str = Field(default="1.0.0")
    DEBUG: bool = Field(default=False)
    ENVIRONMENT: str = Field(default="production")
    
    # Server
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8000)
    
    # Database
    MONGODB_URI: str = Field(default="mongodb://localhost:27017")
    DATABASE_NAME: str = Field(default="resume_interview_db")
    
    # File Upload
    MAX_UPLOAD_SIZE: int = Field(default=5242880)  # 5MB
    ALLOWED_EXTENSIONS: str = Field(default="pdf,docx")
    UPLOAD_DIR: str = Field(default="./uploads")
    
    # NLP
    SPACY_MODEL: str = Field(default="en_core_web_lg")
    
    # CORS
    ALLOWED_ORIGINS: str = Field(
        default="http://localhost:3000,http://localhost:3001"
    )
    
    # Security
    SECRET_KEY: str = Field(default="change-this-in-production")
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO")
    LOG_FILE: str = Field(default="./logs/app.log")
    
    @validator("ALLOWED_EXTENSIONS")
    def validate_extensions(cls, v):
        """Ensure extensions are valid"""
        exts = [ext.strip().lower() for ext in v.split(",")]
        valid_exts = ["pdf", "docx", "doc"]
        for ext in exts:
            if ext not in valid_exts:
                raise ValueError(f"Invalid extension: {ext}")
        return v
    
    @property
    def allowed_extensions_list(self) -> List[str]:
        """Return extensions as a list"""
        return [ext.strip().lower() for ext in self.ALLOWED_EXTENSIONS.split(",")]
    
    @property
    def cors_origins(self) -> List[str]:
        """Return CORS origins as a list"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    def ensure_directories(self):
        """Create necessary directories if they don't exist"""
        Path(self.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
        Path(self.LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()

# Ensure directories exist on import
settings.ensure_directories()
