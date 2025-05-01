from enum import StrEnum

__all__ = [
    "EnvironmentEnum",
]


class EnvironmentEnum(StrEnum):
    development = "development"
    production = "production"
