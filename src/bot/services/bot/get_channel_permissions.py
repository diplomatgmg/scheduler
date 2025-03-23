

from aiogram.types import ChatMemberAdministrator

from bot.core.loader import bot


async def get_channel_permissions(chat_id: int) -> ChatMemberAdministrator:
    return await bot.get_chat_member(chat_id, bot.id)  # type: ignore[return-value]
