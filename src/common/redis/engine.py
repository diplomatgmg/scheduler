from functools import lru_cache
from typing import cast

from loguru import logger
from pydantic import RedisDsn
from redis.asyncio import Redis

from common.redis.enums import RedisDbEnum


__all__ = [
    "get_redis_instance",
]


@lru_cache(maxsize=len(RedisDbEnum))
def get_redis_instance(db: RedisDbEnum) -> Redis:
    try:
        dsn = _get_redis_dsn_by_db(db)
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


def _get_redis_dsn_by_db(db: RedisDbEnum) -> RedisDsn:
    if db == RedisDbEnum.CACHE:
        from common.redis.config import redis_cache_config  # noqa: PLC0415

        return redis_cache_config.connection.dsn

    if db == RedisDbEnum.CELERY:
        from bot.celery.config import celery_config  # noqa: PLC0415

        return celery_config.connection.dsn

    msg = f"Unexpected redis db: {RedisDbEnum}"
    raise ValueError(msg)
