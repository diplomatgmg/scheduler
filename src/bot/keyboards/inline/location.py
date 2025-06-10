from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks.location import LocationActionEnum, LocationCallback


__all__ = [
    "location_selection_keyboard",
    "share_location_keyboard",
    "timezone_offset_selection_keyboard",
]


def location_selection_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📍 Поделиться",
                    callback_data=LocationCallback(action=LocationActionEnum.SHARE_LOCATION).pack(),
                ),
                InlineKeyboardButton(
                    text="🌍 Выбрать",
                    callback_data=LocationCallback(action=LocationActionEnum.CHOOSE_LOCATION).pack(),
                ),
            ]
        ]
    )


def share_location_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📍 Поделиться", request_location=True)]],
        one_time_keyboard=True,
        resize_keyboard=True,
    )


def timezone_offset_selection_keyboard(offsets: list[int]) -> InlineKeyboardMarkup:
    def get_str_offset(value: int) -> str:
        return f"UTC{value}" if value < 0 else f"UTC+{value}"

    buttons = [
        [
            InlineKeyboardButton(
                text=get_str_offset(offset),
                callback_data=LocationCallback(action=LocationActionEnum.CHOOSE_LOCATION, offset=offset).pack(),
            )
        ]
        for offset in offsets
    ]

    return InlineKeyboardBuilder(buttons).as_markup()
