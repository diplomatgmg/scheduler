from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks.post import PostMenuActionEnum, PostMenuCallback


__all__ = [
    "main_keyboard",
]


def main_keyboard() -> InlineKeyboardMarkup:
    """Используется в главном меню или при старте бота."""
    buttons = [
        [
            InlineKeyboardButton(
                text="Создать пост",
                callback_data=PostMenuCallback(action=PostMenuActionEnum.CREATE).pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text="Настройки",
                callback_data=PostMenuCallback(action=PostMenuActionEnum.SETTINGS).pack(),
            ),
            InlineKeyboardButton(
                text="Редактировать",
                callback_data=PostMenuCallback(action=PostMenuActionEnum.EDIT).pack(),
            ),
        ],
    ]

    return InlineKeyboardBuilder(markup=buttons).as_markup()
