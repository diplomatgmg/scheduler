from pydantic import Field, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


__all__ = [
    "redis_config",
]


class RedisConfig(BaseSettings):
    host: str
    port: int = Field(ge=1, le=65535)
    db: int = Field(ge=0)  # FIXME. Не нравится. Можно разделить, например: RedisCacheConfig, RedisCeleryConfig, или использовать Enum
    cache_time: int

    model_config = SettingsConfigDict(env_prefix="REDIS_")

    @property
    def dsn(self) -> RedisDsn:
        return RedisDsn(f"redis://{self.host}:{self.port}/{self.db}")


redis_config = RedisConfig()
