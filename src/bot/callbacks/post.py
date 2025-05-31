from enum import StrEnum

from aiogram.filters.callback_data import CallbackData


__all__ = [
    "PostActionEnum",
    "PostCallback",
    "PostScheduleCallback",
    "PostScheduleEnum",
]


class PostActionEnum(StrEnum):
    CREATE = "create"
    SETTINGS = "settings"
    EDIT = "edit"
    BACK = "back"

    ADD_BUTTONS = "add_buttons"
    CANCEL_ADD_BUTTONS = "cancel_add_buttons"
    REMOVE_BUTTONS = "remove_buttons"

    SCHEDULE_POST = "schedule_post"


class PostCallback(CallbackData, prefix="post"):
    action: PostActionEnum


class PostScheduleEnum(StrEnum):
    PUBLISH_NOW = "publish_now"
    SCHEDULE = "schedule"
    SET_DELETE_TIMER = "set_delete_timer"


class PostScheduleCallback(CallbackData, prefix="post_schedule"):
    action: PostScheduleEnum
