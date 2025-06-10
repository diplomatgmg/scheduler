from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from bot.handlers.utils import show_main_menu
from common.database.services.user.update_user import update_user


__all__ = [
    "update_user_offset",
]


async def update_user_offset(message: Message, session: AsyncSession, user_id: int, offset: int) -> None:
    await update_user(session, user_id, timezone_offset=offset)

    formatted_offset = f"UTC{offset}" if offset < 0 else f"UTC+{offset}"
    update_text = f"✅ Установлена зона: {formatted_offset}"

    try:
        await message.edit_text(update_text)
    except TelegramBadRequest:
        await message.answer(update_text, reply_markup=ReplyKeyboardRemove())

    await show_main_menu(message, delay=1.5)
