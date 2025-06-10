from enum import StrEnum

from aiogram.filters.callback_data import CallbackData


__all__ = [
    "LocationActionEnum",
    "LocationCallback",
]


class LocationActionEnum(StrEnum):
    SHARE_LOCATION = "share_location"
    CHOOSE_LOCATION = "choose_location"


class LocationCallback(CallbackData, prefix="location"):
    action: LocationActionEnum
    offset: int | None = None
