from aiogram.types import CallbackQuery, User

from bot.exceptions import UserNotAvailableError


__all__ = [
    "get_user",
]


async def get_user(event: CallbackQuery) -> User:
    """Возвращает объект пользователя или выбрасывает исключение"""
    user = event.from_user

    if user is None:
        await event.answer("Произошла ошибка. Попробуйте позже.")
        raise UserNotAvailableError

    return user
