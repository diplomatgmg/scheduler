from collections.abc import Awaitable, Callable
from functools import wraps
from typing import Any, Concatenate, ParamSpec, TypeVar, cast

from loguru import logger
from redis.asyncio import Redis

from common.redis.config import redis_cache_config
from common.redis.engine import get_redis_instance
from common.utils.serializers import AbstractSerializer, PickleSerializer


__all__ = [
    "build_key",
    "cache",
    "invalidate_cache",
]


P = ParamSpec("P")
R = TypeVar("R")


def build_key(*args: Any, **kwargs: Any) -> str:
    """Создает ключ для кеширования в Redis."""
    args_str = ":".join(map(str, args))
    kwargs_str = ":".join(f"{key}={value}" for key, value in sorted(kwargs.items()))

    return f"{args_str}:{kwargs_str}"


def get_key_prefix(fn: Callable[..., Any]) -> str:
    """Создает префикс для кешируемого ключа."""
    return f"{fn.__module__}:{fn.__name__}"


async def set_redis_value(
    redis_instance: Redis,
    key: bytes | str,
    value: bytes,
    cache_ttl: int | None = None,
    *,
    is_transaction: bool = False,
) -> None:
    """Кеширует значение по ключу в Redis."""
    async with redis_instance.pipeline(transaction=is_transaction) as pipeline:
        await pipeline.set(key, value)
        logger.debug(f"Set cache. {key=}, {value=}")
        if cache_ttl:
            await pipeline.expire(key, cache_ttl)
        await pipeline.execute()


def cache(
    key_builder: Callable[..., str],
    cache_ttl: int | None = None,
    redis_instance: Redis | None = None,
    serializer: AbstractSerializer | None = None,
) -> Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R]]]:
    """Кеширует результат функции на основе аргументов функции"""
    cache_ttl = cache_ttl or redis_cache_config.ttl
    serializer = serializer or PickleSerializer()
    redis_instance = redis_instance or get_redis_instance(redis_cache_config.connection.dsn)

    def decorator(fn: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        @wraps(fn)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            key_build = key_builder(*args, **kwargs)
            key_prefix = get_key_prefix(fn)
            key = f"{key_prefix}:{key_build}"

            cached_value = await redis_instance.get(key)
            if cached_value is not None:
                logger.debug(f"Getting cache. {key=}")
                return cast("R", serializer.deserialize(cached_value))

            result = await fn(*args, **kwargs)

            await set_redis_value(
                redis_instance,
                key,
                serializer.serialize(result),
                cache_ttl,
            )

            return result

        return wrapper

    return decorator


def invalidate_cache(
    cached_function: Callable[P, Awaitable[R]],
    key_builder: Callable[Concatenate[Any, P], str],
    *,
    redis_instance: Redis | None = None,
) -> Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R]]]:
    """Декоратор для инвалидации кеша."""
    redis_instance = redis_instance or get_redis_instance(redis_cache_config.connection.dsn)

    def decorator(fn: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        @wraps(fn)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            key_build = key_builder(*args, **kwargs)
            key_prefix = get_key_prefix(cached_function)
            key = f"{key_prefix}:{key_build}"

            deleted = await redis_instance.delete(key)
            if deleted:
                logger.debug(f"Invalidated cache for key: {key}")
            else:
                logger.debug(f"No cache to invalidate for key: {key}")

            return await fn(*args, **kwargs)

        return wrapper

    return decorator
