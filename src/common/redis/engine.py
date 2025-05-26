from functools import lru_cache
from typing import cast

from loguru import logger
from redis.asyncio import Redis

from bot.celery.config import celery_config
from common.redis.config import redis_cache_config
from common.redis.enums import RedisDbEnum


__all__ = [
    "get_redis_instance",
]


@lru_cache(maxsize=len(RedisDbEnum))
def get_redis_instance(db: RedisDbEnum) -> Redis:
    match db:
        case RedisDbEnum.CACHE:
            dsn = redis_cache_config.connection.dsn
        case RedisDbEnum.CELERY:
            dsn = celery_config.connection.dsn
        case _:
            msg = f"Unexpected redis db: {RedisDbEnum}"
            raise ValueError(msg)

    try:
        return cast(
            "Redis",
            Redis.from_url(
                str(dsn),
                decode_responses=False,
            ),
        )
    except Exception:
        logger.critical("Не удалось создать экземпляр клиента Redis")
        raise
