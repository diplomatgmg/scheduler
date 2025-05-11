from collections.abc import Awaitable, Callable
from datetime import timedelta
from functools import wraps
from typing import Any, TypeVar

from loguru import logger
from redis.asyncio import Redis

from common.redis.config import redis_config
from common.redis.engine import get_redis_instance
from common.utils.serializers import AbstractSerializer, PickleSerializer


__all__ = [
    "cache",
]


Func = TypeVar("Func")


def build_key(*args: Any, **kwargs: Any) -> str:
    """Создает ключ для кеширования в Redis"""
    args_str = ":".join(map(str, args))
    kwargs_str = ":".join(f"{key}={value}" for key, value in sorted(kwargs.items()))

    return f"{args_str}:{kwargs_str}"


async def set_redis_value(
    key: bytes | str,
    value: bytes,
    cache_time: int | timedelta | None = None,
    *,
    is_transaction: bool = False,
) -> None:
    """Кеширует значение по ключу в Redis"""
    client = get_redis_instance()

    async with client.pipeline(transaction=is_transaction) as pipeline:
        await pipeline.set(key, value)
        logger.debug(f"Закешировано значение. {key=}, {value=}")
        if cache_time:
            await pipeline.expire(key, cache_time)
        await pipeline.execute()


def cache(
    cache_time: int | timedelta | None = None,
    redis_instance: Redis | None = None,
    key_builder: Callable[..., str] = build_key,
    serializer: AbstractSerializer | None = None,
) -> Callable[[Callable[..., Awaitable[Func]]], Callable[..., Awaitable[Func]]]:
    cache_time = cache_time or redis_config.cache_time
    serializer = serializer or PickleSerializer()
    redis_instance = redis_instance or get_redis_instance()

    def decorator(fn: Callable[..., Awaitable[Func]]) -> Callable[..., Awaitable[Func]]:
        @wraps(fn)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            key_build = key_builder(*args, **kwargs)
            key_module = f"{fn.__module__}:{fn.__name__}"
            key = f"{key_module}:{key_build}"

            cached_value = await redis_instance.get(key)
            if cached_value is not None:
                logger.debug(f"Получено кешированное значение. {key=}, {cached_value=}")
                return serializer.deserialize(cached_value)

            result = await fn(*args, **kwargs)

            await set_redis_value(
                key,
                serializer.serialize(result),
                cache_time,
            )

            return result

        return wrapper

    return decorator
