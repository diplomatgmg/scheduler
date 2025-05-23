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

    # FIXME Почему нет задержки? Сколько операций обрабатывается в цикле, если нет апдейтов (насколько нагружает сервер)?
    while True:
        update = await queue.pop(RedisCacheKeyEnum.TELEGRAM_UPDATES)

        if update:
            await dp.feed_raw_update(bot, update)
