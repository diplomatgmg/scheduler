from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

__all__ = [
    "main_keyboard",
]

from bot.callbacks import PostCallback
from bot.callbacks.post import PostActionEnum


def main_keyboard() -> InlineKeyboardMarkup:
    """Используется в главном меню или при старте бота."""
    buttons = [
        [
            InlineKeyboardButton(
                text="Создать пост",
                callback_data=PostCallback(action=PostActionEnum.CREATE).pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text="Настройки",
                callback_data=PostCallback(action=PostActionEnum.SETTINGS).pack(),
            ),
            InlineKeyboardButton(
                text="Редактировать",
                callback_data=PostCallback(action=PostActionEnum.EDIT).pack(),
            ),
        ],
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)

    return keyboard.as_markup()
