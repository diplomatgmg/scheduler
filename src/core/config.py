from enum import Enum

from pydantic_settings import BaseSettings
from pydantic import Field


class EnvironmentEnum(str, Enum):
    development = "development"
    production = "production"


class LogLevelEnum(str, Enum):
    debug = "DEBUG"
    info = "INFO"
    warning = "WARNING"
    error = "ERROR"
    critical = "CRITICAL"


class Settings(BaseSettings):
    ENVIRONMENT: EnvironmentEnum = EnvironmentEnum.development
    LOG_LEVEL: LogLevelEnum = LogLevelEnum.info
    BOT_TOKEN: str = Field(default=...)

    @property
    def DEBUG(self) -> bool:  # noqa
        return self.ENVIRONMENT == EnvironmentEnum.development

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


config = Settings()
