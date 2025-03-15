from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks.menu import MenuCallback, MenuActionEnum


def main_keyboard() -> InlineKeyboardMarkup:
    """Используется в главно меню или при старте бота."""
    buttons = [
        [
            InlineKeyboardButton(
                text="Настройки",
                callback_data=MenuCallback(action=MenuActionEnum.SETTINGS).pack(),
            )
        ],
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)

    keyboard.adjust(1, 1, 2)

    return keyboard.as_markup()
