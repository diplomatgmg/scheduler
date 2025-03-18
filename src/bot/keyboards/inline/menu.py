from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks.menu import MenuActionEnum, MenuCallback

if TYPE_CHECKING:
    from aiogram.types import InlineKeyboardMarkup


def main_keyboard() -> InlineKeyboardMarkup:
    """Используется в главно меню или при старте бота."""
    buttons = [
        [
            InlineKeyboardButton(
                text="Настройки",
                callback_data=MenuCallback(action=MenuActionEnum.SETTINGS).pack(),
            ),
        ],
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)

    keyboard.adjust(1, 1, 2)

    return keyboard.as_markup()
