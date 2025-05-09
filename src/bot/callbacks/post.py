from enum import StrEnum

from aiogram.filters.callback_data import CallbackData


__all__ = [
    "PostActionEnum",
    "PostCallback",
]


class PostActionEnum(StrEnum):
    CREATE = "create"
    SETTINGS = "settings"
    EDIT = "edit"
    BACK = "back"


class PostCallback(CallbackData, prefix="post"):
    action: PostActionEnum
