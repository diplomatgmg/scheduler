from enum import StrEnum

from aiogram.filters.callback_data import CallbackData


__all__ = [
    "PostMenuActionEnum",
    "PostMenuCallback",
]


class PostMenuActionEnum(StrEnum):
    CREATE = "create"
    SETTINGS = "settings"
    EDIT = "edit"


class PostMenuCallback(CallbackData, prefix="post"):
    action: PostMenuActionEnum
