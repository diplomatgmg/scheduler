from aiogram.types import Message, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from bot.handlers.utils import show_main_menu
from common.database.models import UserModel
from common.database.services.user import update_user


__all__ = [
    "update_user_offset",
]


async def update_user_offset(
    message: Message, session: AsyncSession, user: UserModel, offset: int, *, edit_message: bool = False
) -> None:
    await update_user(session, user, timezone_offset=offset)

    formatted_offset = f"UTC{int(offset)}" if offset < 0 else f"UTC+{int(offset)}"
    update_text = f"✅ Установлена зона: {formatted_offset}"

    if edit_message:
        await message.edit_text(update_text)
    else:
        await message.answer(update_text, reply_markup=ReplyKeyboardRemove())

    await show_main_menu(message, delay=1.5)
