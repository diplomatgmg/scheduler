from pydantic_settings import BaseSettings, SettingsConfigDict

from common.logging.enums import LogLevelEnum, LogLevelSqlalchemyEnum


__all__ = [
    "log_config",
]


class LogConfig(BaseSettings):
    level: LogLevelEnum
    sqlalchemy_level: LogLevelSqlalchemyEnum

    model_config = SettingsConfigDict(env_prefix="LOG_")


log_config = LogConfig()
