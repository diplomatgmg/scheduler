from enum import StrEnum

from aiogram.filters.callback_data import CallbackData


__all__ = [
    "PostCreateActionEnum",
    "PostCreateCallback",
]


class PostCreateActionEnum(StrEnum):
    BACK = "back"

    ADD_BUTTONS = "add_buttons"
    CANCEL_ADD_BUTTONS = "cancel_add_buttons"
    REMOVE_BUTTONS = "remove_buttons"

    SCHEDULE = "schedule"


class PostCreateCallback(CallbackData, prefix="post"):
    action: PostCreateActionEnum
