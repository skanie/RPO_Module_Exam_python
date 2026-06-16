from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "exam_password"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "nexus_db"
    SECRET_KEY: str = "super_secret_exam_key_123"

    class Config:
        env_file = "backend/.env"

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
