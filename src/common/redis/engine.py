from functools import lru_cache
from typing import cast

from loguru import logger
from redis.asyncio import Redis

from common.redis.config import redis_config


__all__ = [
    "get_redis_instance",
]


@lru_cache(maxsize=1)
def get_redis_instance() -> Redis:
    try:
        return cast(
            "Redis",
            Redis.from_url(
                str(redis_config.dsn),
                decode_responses=False,
            ),
        )
    except Exception:
        logger.critical("Не удалось создать экземпляр клиента Redis")
        raise
