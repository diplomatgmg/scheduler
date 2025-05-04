from aiogram.filters.callback_data import CallbackQuery
from aiogram.types import Chat, ChatMemberUpdated, Message, User


__all__ = [
    "get_username",
]


def _extract_entity(entity: User | Message | Chat | CallbackQuery | ChatMemberUpdated) -> User | Chat | None:
    """Извлекает объект Chat/User из переданной сущности."""
    if isinstance(entity, (User, Chat)):
        return entity
    if isinstance(entity, (Message, CallbackQuery)):
        return entity.from_user
    if isinstance(entity, ChatMemberUpdated):
        return entity.chat

    return None


def get_username(entity: User | Chat | Message | CallbackQuery | ChatMemberUpdated) -> str | None:
    """Возвращает username объекта если он существует."""
    subject = _extract_entity(entity)
    if subject is None:
        return None

    username = subject.username
    if not username:
        return None

    return username
