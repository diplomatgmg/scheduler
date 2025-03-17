from aiogram.filters import ADMINISTRATOR, ChatMemberUpdatedFilter
from aiogram.types import ChatMemberUpdated
from loguru import logger

from bot.core.loader import bot, dp


@dp.chat_member_handler(ChatMemberUpdatedFilter(member_status_changed=ADMINISTRATOR))
async def on_bot_promoted(event: ChatMemberUpdated) -> None:
    chat_id = event.chat.id
    chat_title = event.chat.title or "Без названия"

    logger.info(f"Bot promoted to admin in channel: {chat_title} (ID: {chat_id})")

    await bot.send_message(
        event.from_user.id, f"Бот стал администратором в канале: {chat_title}",
    )
