from enum import StrEnum

from aiogram.filters.callback_data import CallbackData


__all__ = [
    "PostScheduleActionEnum",
    "PostScheduleCallback",
]


class PostScheduleActionEnum(StrEnum):
    PUBLISH_NOW = "publish_now"
    SCHEDULE = "schedule"
    SET_DELETE_TIMER = "set_delete_timer"


class PostScheduleCallback(CallbackData, prefix="post_schedule"):
    action: PostScheduleActionEnum
