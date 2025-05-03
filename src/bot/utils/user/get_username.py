from aiogram.filters.callback_data import CallbackQuery
from aiogram.types import Chat, ChatMemberUpdated, Message, User
from loguru import logger


__all__ = [
    "get_username",
]


def _extract_user(entity: User | Message | Chat | CallbackQuery | ChatMemberUpdated) -> User | Chat | None:
    """
    Извлекает объект User из переданной сущности.
    """
    if isinstance(entity, User):
        return entity
    if isinstance(entity, Chat):
        return entity
    if isinstance(entity, Message):
        return entity.from_user
    if isinstance(entity, CallbackQuery):
        return entity.from_user
    if isinstance(entity, ChatMemberUpdated):
        return entity.chat

    return None


def get_username(entity: User | Chat | Message | CallbackQuery | ChatMemberUpdated) -> str:
    """
    Возвращает username пользователя в формате '@username'.
    Если username не найден — логирует и возвращает 'unknown'.
    """
    user = _extract_user(entity)

    if user is None:
        logger.error(f"Cannot extract User from entity: {entity!r}")
        return "unknown"

    username = user.username
    if not username:
        logger.error(f"User has no username: {user!r}")
        return "unknown"

    return f"@{username}"
