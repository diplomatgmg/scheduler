from enum import Enum

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings
from sqlalchemy import URL


class EnvironmentEnum(str, Enum):
    development = "development"
    production = "production"


class LogLevelEnum(str, Enum):
    debug = "DEBUG"
    info = "INFO"
    warning = "WARNING"
    error = "ERROR"
    critical = "CRITICAL"


class DBSettings(BaseSettings):
    user: str = Field(default=..., alias="POSTGRES_USER")
    password: SecretStr = Field(default=..., alias="POSTGRES_PASSWORD")
    host: str = Field(default=..., alias="POSTGRES_HOST")
    port: int = Field(default=..., alias="POSTGRES_PORT")
    name: str = Field(default=..., alias="POSTGRES_NAME")

    @property
    def url(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.user,
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            database=self.name,
        )


class Settings(BaseSettings):
    ENVIRONMENT: EnvironmentEnum = EnvironmentEnum.development
    LOG_LEVEL: LogLevelEnum = LogLevelEnum.info
    BOT_TOKEN: str = Field(default=...)
    DB: DBSettings = DBSettings()

    @property
    def DEBUG(self) -> bool:  # noqa
        return self.ENVIRONMENT == EnvironmentEnum.development

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
