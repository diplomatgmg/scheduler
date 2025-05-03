from pydantic_settings import BaseSettings

from common.logging.enums import LogLevelEnum, LogLevelSqlalchemyEnum


__all__ = [
    "log_config",
]


class LogConfig(BaseSettings):
    level: LogLevelEnum
    sqlalchemy_level: LogLevelSqlalchemyEnum

    class Config:
        env_prefix = "LOG_"


log_config = LogConfig()  # type: ignore[call-arg]
