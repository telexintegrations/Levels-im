from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
  # API settings
  REDIS_URL: str
  REDIS_URL_BE: str | None = None
  
  class Config:
    case_sensitive = True
    env_file = ".env"

settings = Settings()