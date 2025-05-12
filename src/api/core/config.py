from pydantic import Field, IPvAnyAddress
from pydantic_settings import BaseSettings, SettingsConfigDict


__all__ = [
    "api_config",
]


class ApiConfig(BaseSettings):
    host: IPvAnyAddress
    port: int = Field(ge=1, le=65535)

    model_config = SettingsConfigDict(env_prefix="API_")


api_config = ApiConfig()
