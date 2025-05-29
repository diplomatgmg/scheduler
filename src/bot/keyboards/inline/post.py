from collections.abc import Sequence

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks import PostCallback, SelectChannelCallback
from bot.callbacks.post import PostActionEnum
from common.database.models import ChannelModel


__all__ = [
    "post_additional_configuration",
    "post_cancel_buttons",
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

    return InlineKeyboardBuilder(buttons).as_markup()


def post_additional_configuration(
    saved_buttons: list[list[InlineKeyboardButton]] | None = None,
) -> InlineKeyboardMarkup:
    """Дополнительная настройка поста перед отложкой"""
    builder = InlineKeyboardBuilder()

    if saved_buttons is not None:
        for row in saved_buttons:
            builder.row(*row)

    builder.row(
        InlineKeyboardButton(
            text="-----------------------",
            callback_data="noop",
        )
    )

    if saved_buttons is not None:
        builder.row(
            InlineKeyboardButton(
                text="Удалить URL-кнопки", callback_data=PostCallback(action=PostActionEnum.REMOVE_BUTTONS).pack()
            )
        )
    else:
        builder.row(
            InlineKeyboardButton(
                text="Добавить URL-кнопки", callback_data=PostCallback(action=PostActionEnum.ADD_BUTTONS).pack()
            )
        )

    return builder.as_markup()


def post_cancel_buttons() -> InlineKeyboardMarkup:
    """Отменяет создание URL кнопок"""
    buttons = [
        [
            InlineKeyboardButton(
                text="Отменить создание кнопок",
                callback_data=PostCallback(action=PostActionEnum.CANCEL_ADD_BUTTONS).pack(),  # FIXME для чего .pack()?
            )
        ]
    ]

    return InlineKeyboardBuilder(buttons).as_markup()
