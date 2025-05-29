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

    ADD_BUTTONS = "add_buttons"
    CANCEL_ADD_BUTTONS = "cancel_add_buttons"
    REMOVE_BUTTONS = "remove_buttons"


class PostCallback(CallbackData, prefix="post"):
    action: PostActionEnum
