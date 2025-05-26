from bot.core.loader import bot, dp
from common.redis.client import RedisQueueClient
from common.redis.enums import RedisCacheKeyEnum


__all__ = [
    "start_redis_consumer",
]


# FIXME вынести в src.tasks??
async def start_redis_consumer() -> None:
    """Получает updates с очереди Redis и передает их в Dispatcher"""
    queue = RedisQueueClient()

    while True:
        update = await queue.pop(RedisCacheKeyEnum.TELEGRAM_UPDATES)

        if not isinstance(update, dict):
            msg = f"Unexpected update  format. type={type(update)}, data={update}"
            raise TypeError(msg)

        await dp.feed_raw_update(bot, update)
