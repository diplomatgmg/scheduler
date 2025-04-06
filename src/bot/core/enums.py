from enum import StrEnum


class EnvironmentEnum(StrEnum):
    development = "development"
    production = "production"


class LogLevelEnum(StrEnum):
    debug = "DEBUG"
    info = "INFO"
    warning = "WARNING"
    error = "ERROR"
    critical = "CRITICAL"
