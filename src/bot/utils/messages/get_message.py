from aiogram.types import CallbackQuery, Message

from bot.exceptions import MessageNotAvailableError


__all__ = [
    "get_message",
]


async def get_message(query: CallbackQuery) -> Message:
    """Возвращает объект сообщения или выбрасывает исключение"""
    if isinstance(query.message, Message):
        return query.message

    await query.answer("Произошла ошибка. Попробуйте позже.")

    raise MessageNotAvailableError
