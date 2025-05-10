from pydantic import Field
from pydantic_settings import BaseSettings


__all__ = [
    "redis_config",
]


class RedisConfig(BaseSettings):
    host: str
    port: int = Field(ge=1, le=65535)

    class Config:
        env_prefix = "REDIS_"


redis_config = RedisConfig()
