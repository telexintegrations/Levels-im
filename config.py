from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
  # API settings
  REDIS_URL: str = 'redis://localhost:6379/0'
  REDIS_URL_BE: str | None = None
  
  class Config:
    case_sensitive = True
    env_file = ".env"

settings = Settings()