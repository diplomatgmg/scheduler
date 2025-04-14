from enum import StrEnum

from pydantic_settings import BaseSettings

__all__ = [
    "LogLevelEnum",
    "LogLevelSqlalchemyEnum",
    "LogSettings",
]


class LogLevelEnum(StrEnum):
    debug = "DEBUG"
    info = "INFO"
    warning = "WARNING"
    error = "ERROR"
    critical = "CRITICAL"


class LogLevelSqlalchemyEnum(StrEnum):
    debug = "DEBUG"
    info = "INFO"
    warning = "WARNING"


class LogSettings(BaseSettings):
    level: LogLevelEnum
    sqlalchemy_level: LogLevelSqlalchemyEnum

    class Config:
        env_prefix = "LOG_"
