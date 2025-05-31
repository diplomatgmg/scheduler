from pydantic import Field, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

from common.redis.enums import RedisDbEnum


__all__ = [
    "RedisConnectionConfig",
    "redis_cache_config",
]


class RedisConnectionConfig(BaseSettings):
    host: str
    port: int = Field(ge=1, le=65535)
    db: RedisDbEnum = Field(RedisDbEnum.NOT_SET)

    model_config = SettingsConfigDict(env_prefix="REDIS_")

    @property
    def dsn(self) -> RedisDsn:
        if self.db == RedisDbEnum.NOT_SET:
            msg = "Redis DB not configured"
            raise ValueError(msg)

        return RedisDsn(f"redis://{self.host}:{self.port}/{self.db}")


class RedisCacheConfig(BaseSettings):
    connection: RedisConnectionConfig = RedisConnectionConfig(db=RedisDbEnum.CACHE)

    ttl: int

    model_config = SettingsConfigDict(env_prefix="REDIS_CACHE_")


redis_cache_config = RedisCacheConfig()
