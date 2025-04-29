from collections.abc import Sequence

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.db.models import ChannelModel
from bot.schemas.menu import ChannelSelectCallback, MenuActionEnum, MenuCallback

__all__ = [
    "main_keyboard",
    "select_another_channel_keyboard",
    "select_channel_keyboard",
]

# FIXME Реструктурировать


def main_keyboard() -> InlineKeyboardMarkup:
    """Используется в главном меню или при старте бота."""
    buttons = [
        [
            InlineKeyboardButton(
                text="Создать пост",
                callback_data=MenuCallback(action=MenuActionEnum.CREATE).pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text="Настройки",
                callback_data=MenuCallback(action=MenuActionEnum.SETTINGS).pack(),
            ),
            InlineKeyboardButton(
                text="Редактировать",
                callback_data=MenuCallback(action=MenuActionEnum.EDIT).pack(),
            ),
        ],
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)
    return keyboard.as_markup()


def select_channel_keyboard(channels: Sequence[ChannelModel]) -> InlineKeyboardMarkup:
    """Используется для выбора канала, в котором необходимо создать пост"""
    # FIXME Зачем тут builder? Обычного list comprehensions не хватает?
    builder = InlineKeyboardBuilder()

    buttons = [
        InlineKeyboardButton(
            text=channel.title,
            callback_data=ChannelSelectCallback(channel_title=channel.title, channel_username=channel.username).pack(),
        )
        for channel in channels
    ]

    builder.add(*buttons)
    builder.add(
        InlineKeyboardButton(
            text="← Назад",
            callback_data=MenuCallback(action=MenuActionEnum.BACK).pack(),
        )
    )

    builder.adjust(1)

    return builder.as_markup()


def select_another_channel_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text="Выбрать другой канал", callback_data=MenuCallback(action=MenuActionEnum.CREATE).pack()
            )
        ]
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)
    return keyboard.as_markup()
