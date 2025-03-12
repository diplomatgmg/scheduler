from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


config = Settings()
