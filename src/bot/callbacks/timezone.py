from aiogram.filters.callback_data import CallbackData


__all__ = ["TimezoneCallback"]


class TimezoneCallback(CallbackData, prefix="timezone"):
    offset: int
