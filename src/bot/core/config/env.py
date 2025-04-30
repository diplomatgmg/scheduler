from enum import StrEnum

from pydantic_settings import BaseSettings

__all__ = [
    "EnvConfig",
    "EnvironmentEnum",
]


class EnvironmentEnum(StrEnum):
    development = "development"
    production = "production"


class EnvConfig(BaseSettings):
    mode: EnvironmentEnum

    class Config:
        env_prefix = "ENV_"
