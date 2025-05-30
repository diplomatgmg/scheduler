from typing import TYPE_CHECKING, Any, cast

from loguru import logger
from redis.asyncio import Redis
from redis.exceptions import RedisError

from common.redis.config import redis_cache_config
from common.redis.engine import get_redis_instance
from common.redis.enums import RedisCacheKeyEnum
from common.utils.serializers import AbstractSerializer, JSONSerializer


if TYPE_CHECKING:
    from collections.abc import Awaitable


__all__ = [
    "RedisQueueClient",
]


class RedisQueueClient:
    """Клиент для работы с очередями в Redis"""

    _client: Redis

    def __init__(self, client: Redis | None = None, serializer: AbstractSerializer | None = None) -> None:
        self._client = client or get_redis_instance(redis_cache_config.connection.dsn)
        self._serializer = serializer or JSONSerializer()

    async def push(self, key: RedisCacheKeyEnum, data: Any) -> None:
        value_bytes = self._serializer.serialize(data)

        try:
            await cast("Awaitable[int]", self._client.rpush(str(key), value_bytes))
            logger.debug(f"Redis push key={key}")
        except RedisError as e:
            logger.error(f"Redis push failed for key={key}: {e}")
            raise

    async def pop(self, key: RedisCacheKeyEnum) -> Any | None:
        try:
            result = await cast("Awaitable[list[bytes] | None]", self._client.blpop([str(key)], timeout=1))
            if result is None:
                return None

            _, data_bytes = result
            logger.debug(f"Popped update from Redis list key={key}")

            return self._serializer.deserialize(data_bytes)

        except RedisError as e:
            logger.error(f"Redis pop failed for key={key}: {e}")
            raise
