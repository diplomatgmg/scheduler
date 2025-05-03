from aiogram.filters.callback_data import CallbackData

__all__ = [
    "SelectChannelCallback",
]


class SelectChannelCallback(CallbackData, prefix="select_channel"):
    channel_title: str
    channel_username: str | None
