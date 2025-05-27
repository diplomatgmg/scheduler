from collections.abc import Sequence

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks import PostCallback, SelectChannelCallback
from bot.callbacks.post import PostActionEnum
from common.database.models import ChannelModel


__all__ = [
    "select_another_channel_keyboard",
    "select_channel_keyboard",
]


def select_channel_keyboard(channels: Sequence[ChannelModel]) -> InlineKeyboardMarkup:
    """Используется для выбора канала, в котором необходимо создать пост"""
    keyboard = InlineKeyboardBuilder()

    buttons = [
        InlineKeyboardButton(
            text=channel.title,
            callback_data=SelectChannelCallback(
                chat_id=channel.chat_id, channel_title=channel.title, channel_username=channel.username
            ).pack(),
        )
        for channel in channels
    ]

    keyboard.add(*buttons)
    keyboard.add(
        InlineKeyboardButton(
            text="← Назад",
            callback_data=PostCallback(action=PostActionEnum.BACK).pack(),
        )
    )

    keyboard.adjust(1)

    return keyboard.as_markup()


def select_another_channel_keyboard() -> InlineKeyboardMarkup:
    """Используется для выбора другого канала"""
    buttons = [
        [
            InlineKeyboardButton(
                text="Выбрать другой канал", callback_data=PostCallback(action=PostActionEnum.CREATE).pack()
            )
        ]
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)

    return keyboard.as_markup()
