from pydantic_settings import BaseSettings, SettingsConfigDict

from common.environment.enums import EnvironmentEnum


__all__ = [
    "env_config",
]


class EnvConfig(BaseSettings):
    mode: EnvironmentEnum
    project_name: str

    model_config = SettingsConfigDict(env_prefix="ENV_")

    @property
    def debug(self) -> bool:
        return EnvironmentEnum.development == self.mode


env_config = EnvConfig()
