from functools import lru_cache
from typing import cast

from loguru import logger
from pydantic import RedisDsn
from redis.asyncio import Redis

from common.redis.enums import RedisDbEnum


__all__ = [
    "get_redis_instance",
]


def _get_lru_cache_max_size() -> int:
    """Получает размер кеша на основе количества используемых баз данных Redis"""
    return sum(1 for e in RedisDbEnum if e.value > 0)


@lru_cache(maxsize=_get_lru_cache_max_size())
def get_redis_instance(dsn: RedisDsn) -> Redis:
    try:
        redis_client = Redis.from_url(
            str(dsn),
            decode_responses=False,
        )
        return cast("Redis", redis_client)
    except Exception:
        logger.critical("Не удалось создать экземпляр клиента Redis")
        raise
