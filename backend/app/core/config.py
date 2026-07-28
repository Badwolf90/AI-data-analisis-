import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Data Analysis Platform API"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "supersecretjwtkeyforaidataanalysisplatformchangeinproduction"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    DATABASE_URL: str = "sqlite+aiosqlite:///./ai_platform.db"

    UPLOAD_DIR: str = "./uploads"
    MODEL_DIR: str = "./models_registry"
    REPORT_DIR: str = "./generated_reports"

    RATE_LIMIT_PER_MINUTE: int = 100
    ALLOWED_HOSTS: List[str] = ["*"]

    # 9Router AI Gateway Configuration
    NINEROUTER_BASE_URL: str = "http://localhost:20128/v1"
    NINEROUTER_MODEL: str = "ag/gemini-3.5-flash-low"
    NINEROUTER_ENABLED: bool = True

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")



settings = Settings()

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.MODEL_DIR, exist_ok=True)
os.makedirs(settings.REPORT_DIR, exist_ok=True)
