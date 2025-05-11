from enum import StrEnum


__all__ = [
    "RedisCacheKeyEnum",
]


class RedisCacheKeyEnum(StrEnum):
    TELEGRAM_UPDATES = "telegram:updates"
