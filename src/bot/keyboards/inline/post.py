from collections.abc import Sequence

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks import SelectChannelCallback
from bot.callbacks.post import (
    PostCreateActionEnum,
    PostCreateCallback,
    PostMenuActionEnum,
    PostMenuCallback,
    PostScheduleActionEnum,
    PostScheduleCallback,
)
from common.database.models import ChannelModel


__all__ = [
    "post_additional_configuration_keyboard",
    "post_cancel_buttons",
    "scheduling_options_keyboard",
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
            callback_data=PostCreateCallback(action=PostCreateActionEnum.BACK).pack(),
        )
    )

    keyboard.adjust(1)

    return keyboard.as_markup()


def select_another_channel_keyboard() -> InlineKeyboardMarkup:
    """Используется для выбора другого канала"""
    buttons = [
        [
            InlineKeyboardButton(
                text="Выбрать другой канал",
                callback_data=PostMenuCallback(action=PostMenuActionEnum.CREATE).pack(),
            )
        ]
    ]

    return InlineKeyboardBuilder(buttons).as_markup()


def post_additional_configuration_keyboard(
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
                text="Удалить URL-кнопки",
                callback_data=PostCreateCallback(action=PostCreateActionEnum.REMOVE_BUTTONS).pack(),
            )
        )
    else:
        builder.row(
            InlineKeyboardButton(
                text="Добавить URL-кнопки",
                callback_data=PostCreateCallback(action=PostCreateActionEnum.ADD_BUTTONS).pack(),
            )
        )

    builder.row(
        InlineKeyboardButton(
            text="-----------------------",
            callback_data="noop",
        )
    )

    builder.row(
        InlineKeyboardButton(
            text="Далее", callback_data=PostCreateCallback(action=PostCreateActionEnum.SCHEDULE).pack()
        )
    )

    return builder.as_markup()


def post_cancel_buttons() -> InlineKeyboardMarkup:
    """Отменяет создание URL кнопок"""
    buttons = [
        [
            InlineKeyboardButton(
                text="Отменить создание кнопок",
                callback_data=PostCreateCallback(action=PostCreateActionEnum.CANCEL_ADD_BUTTONS).pack(),
            )
        ]
    ]

    return InlineKeyboardBuilder(buttons).as_markup()


def scheduling_options_keyboard() -> InlineKeyboardMarkup:
    """"""
    buttons = [
        [
            InlineKeyboardButton(
                text="Опубликовать",
                callback_data=PostScheduleCallback(action=PostScheduleActionEnum.PUBLISH_NOW).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="Отложить",
                callback_data=PostScheduleCallback(action=PostScheduleActionEnum.SCHEDULE).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="Задать таймер для удаления",
                callback_data=PostScheduleCallback(action=PostScheduleActionEnum.SET_DELETE_TIMER).pack(),
            )
        ],
    ]

    return InlineKeyboardBuilder(buttons).as_markup()
