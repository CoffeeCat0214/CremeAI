from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    DYNAMODB_TABLE: str = "creme_brulee_chat_history"
    DISCORD_TOKEN: str
    ENVIRONMENT: str = "development"
    JWT_SECRET_KEY: str
    API_KEY: str
    MAX_REQUEST_SIZE_MB: int = 1
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/1"
    WEBHOOK_TIMEOUT: int = 5  # seconds
    DISCORD_PUBLIC_KEY: str
    DISCORD_BOT_TOKEN: str
    DISCORD_APPLICATION_ID: str
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings() 