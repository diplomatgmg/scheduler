from aiogram.filters.callback_data import CallbackData

__all__ = [
    "SelectChannelCallback",
]


class SelectChannelCallback(CallbackData, prefix="select_channel"):
    channel_title: str
    # FIXME Почему None? может сделать функцию для обработки? Каждый пользователь/канал имеет username
    channel_username: str | None
