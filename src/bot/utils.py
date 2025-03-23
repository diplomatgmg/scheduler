from __future__ import annotations

from aiogram.filters.callback_data import CallbackQuery
from aiogram.types import Chat, ChatMemberUpdated, Message, User


def get_username(entity: User | Message | CallbackQuery | ChatMemberUpdated | None) -> str:
    """
    Возвращает имя пользователя или 'unknown',
    если пользователь отсутствует или не имеет username.
    """
    user: User | Chat | None = None

    if isinstance(entity, Message):
        user = entity.from_user
    elif isinstance(entity, User):
        user = entity
    elif isinstance(entity, CallbackQuery):
        user = entity.from_user
    elif isinstance(entity, ChatMemberUpdated):
        user = entity.chat

    username = user and user.username
    return f"@{username}" if username is not None else "unknown"
