from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks.timezone import TimezoneCallback
from bot.schemas.location import LocationButtonTextEnum


__all__ = [
    "location_selection_keyboard",
    "timezone_offset_selection_keyboard",
]


def location_selection_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=LocationButtonTextEnum.SHARE_LOCATION, request_location=True),
                KeyboardButton(text=LocationButtonTextEnum.CHOOSE_MANUALLY),
            ]
        ],
        one_time_keyboard=True,
        resize_keyboard=True,
    )


def timezone_offset_selection_keyboard(offsets: list[int]) -> InlineKeyboardMarkup:
    def get_str_offset(value: int) -> str:
        return f"UTC{value}" if value < 0 else f"UTC+{value}"

    buttons = [
        [InlineKeyboardButton(text=get_str_offset(offset), callback_data=TimezoneCallback(offset=offset).pack())]
        for offset in offsets
    ]

    return InlineKeyboardBuilder(buttons).as_markup()
