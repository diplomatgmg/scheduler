from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks.menu import MenuActionEnum, MenuCallback


def main_keyboard() -> InlineKeyboardMarkup:
    """Используется в главном меню или при старте бота."""
    buttons = [
        [
            InlineKeyboardButton(
                text="Создать пост",
                callback_data=MenuCallback(action=MenuActionEnum.SETTINGS).pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text="Отложенные",
                callback_data=MenuCallback(action=MenuActionEnum.SETTINGS).pack(),
            ),
            InlineKeyboardButton(
                text="Редактировать",
                callback_data=MenuCallback(action=MenuActionEnum.SETTINGS).pack(),
            ),
        ],
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)
    return keyboard.as_markup()
