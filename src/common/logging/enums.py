from enum import StrEnum


__all__ = [
    "LogLevelEnum",
    "LogLevelSqlalchemyEnum",
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
