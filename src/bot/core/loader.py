from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage

from bot.core.config import bot_config
from bot.core.storage_config import bot_storage_config
from common.redis.engine import get_redis_instance


__all__ = [
    "bot",
    "dp",
]


storage = RedisStorage(
    redis=get_redis_instance(bot_storage_config.connection.dsn),
    key_builder=DefaultKeyBuilder(with_bot_id=True),
    state_ttl=bot_storage_config.ttl,
    data_ttl=bot_storage_config.ttl,
)


bot = Bot(token=bot_config.token)
dp = Dispatcher(storage=storage)
