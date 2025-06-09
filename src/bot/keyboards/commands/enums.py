from enum import StrEnum


__all__ = ["DefaultCommandEnum"]


class DefaultCommandEnum(StrEnum):
    START = "start"
    SET_TIMEZONE = "set_timezone"
    SUPPORT = "support"
