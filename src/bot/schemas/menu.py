from enum import StrEnum

from aiogram.filters.callback_data import CallbackData

__all__ = [
    "ChannelSelectCallback",
    "MenuActionEnum",
    "MenuCallback",
]


class MenuActionEnum(StrEnum):
    CREATE = "create"
    SETTINGS = "settings"
    EDIT = "edit"
    BACK = "back"


class MenuCallback(CallbackData, prefix="menu"):
    action: MenuActionEnum


class ChannelSelectCallback(CallbackData, prefix="select_channel"):
    channel_title: str  # FIXME use channel id?
    channel_username: str | None
