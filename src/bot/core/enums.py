from enum import StrEnum

__all__ = [
    "EnvironmentEnum",
    "LogLevelEnum",
    "LogLevelSqlalchemyEnum",
]


class EnvironmentEnum(StrEnum):
    development = "development"
    production = "production"


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
