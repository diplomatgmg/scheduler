import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = os.getenv("BUILD_TARGET") == "development"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


config = Settings()
