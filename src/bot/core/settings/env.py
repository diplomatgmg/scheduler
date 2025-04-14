from enum import StrEnum

from pydantic_settings import BaseSettings

__all__ = [
    "EnvSettings",
    "EnvironmentEnum",
]


class EnvironmentEnum(StrEnum):
    development = "development"
    production = "production"


class EnvSettings(BaseSettings):
    mode: EnvironmentEnum

    class Config:
        env_prefix = "ENV_"
