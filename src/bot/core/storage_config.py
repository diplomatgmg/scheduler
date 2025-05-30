from pydantic_settings import BaseSettings, SettingsConfigDict

from common.redis.config import RedisConnectionConfig
from common.redis.enums import RedisDbEnum


__all__ = [
    "bot_storage_config",
]


class BotStorageConfig(BaseSettings):
    connection: RedisConnectionConfig = RedisConnectionConfig(db=RedisDbEnum.BOT_STORAGE)

    ttl: int

    model_config = SettingsConfigDict(env_prefix="BOT_STORAGE_")


bot_storage_config = BotStorageConfig()
