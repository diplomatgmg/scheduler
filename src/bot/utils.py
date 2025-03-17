from aiogram.filters.callback_data import CallbackQuery
from aiogram.types import Message, User


def get_username(entity: User | Message | CallbackQuery | None) -> str:
    """
    Возвращает имя пользователя или 'unknown',
    если пользователь отсутствует или не имеет username.
    """
    if isinstance(entity, Message):
        user = entity.from_user
    elif isinstance(entity, User):
        user = entity
    elif isinstance(entity, CallbackQuery):
        user = entity.from_user
    else:
        user = None

    username = user and user.username
    return f"@{username}" if username else "unknown"
