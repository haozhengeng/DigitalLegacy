from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """应用配置，支持从 .env 文件读取"""
    APP_NAME: str = "DigitalLegacy"
    DEBUG: bool = True

    DATABASE_URL: str = "sqlite+aiosqlite:///./digital_legacy.db"

    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    class Config:
        env_file = ".env"


settings = Settings()
