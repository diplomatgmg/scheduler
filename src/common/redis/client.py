import json
from typing import Any, TypeVar, cast

from loguru import logger
from redis.asyncio import Redis
from redis.exceptions import RedisError

from common.redis.engine import get_redis_instance
from common.redis.enums import RedisCacheKeyEnum


__all__ = [
    "RedisQueueClient",
]

T = TypeVar("T")


class RedisQueueClient:
    """Клиент для работы с очередями в Redis"""
    _client: Redis

    def __init__(self, client: Redis | None = None) -> None:
        self._client = client or get_redis_instance()

    async def push(self, key: RedisCacheKeyEnum, data: Any) -> None:
        if isinstance(data, dict):
            value_bytes = json.dumps(data).encode()
        elif isinstance(data, str):
            value_bytes = data.encode()
        else:
            msg = f"Неподдерживаемый тип данных для кеширования: {type(data)}"
            raise TypeError(msg)

        if not isinstance(value_bytes, bytes):
            msg = f"Тип данных для кеширования должен быть {bytes}"
            raise TypeError(msg)

        try:
            await cast("Any", self._client.rpush)(str(key), value_bytes)
            logger.debug(f"Redis push: {key}")
        except RedisError as e:
            logger.error(f"Redis push failed for {key}: {e}")
            raise

    async def pop(self, key: RedisCacheKeyEnum, expected_type: type[T]) -> T | None:
        try:
            value_bytes = await cast("Any", self._client.lpop)(str(key))
            if value_bytes is None:
                return None

            logger.debug(f"Popped update from Redis list {key}")

            if not isinstance(value_bytes, bytes):
                msg = f"Ожидался тип {bytes}, получен {type(value_bytes).__name__}"
                raise TypeError(msg)

            decoded = value_bytes.decode()
            if expected_type is dict:
                return cast("T", json.loads(decoded))
            if expected_type is str:
                return cast("T", decoded)

            msg = f"Неожиданный тип: {expected_type}"
            raise TypeError(msg)

        except RedisError as e:
            logger.error(f"Redis pop failed for {key}: {e}")
            raise
