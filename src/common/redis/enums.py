from enum import IntEnum, StrEnum


__all__ = [
    "RedisCacheKeyEnum",
    "RedisDbEnum",
]


class RedisDbEnum(IntEnum):
    NOT_SET = 0  # FIXME -1?
    CACHE = 1
    CELERY = 2


class RedisCacheKeyEnum(StrEnum):
    TELEGRAM_UPDATES = "telegram:updates"
