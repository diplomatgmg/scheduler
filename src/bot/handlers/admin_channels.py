# from bot.core.db import db

from aiogram.filters import ChatMemberUpdatedFilter, ADMINISTRATOR
from aiogram.types import ChatMemberUpdated
from loguru import logger

from bot.core.loader import dp, bot


@dp.chat_member_handler(ChatMemberUpdatedFilter(member_status_changed=ADMINISTRATOR))
async def on_bot_promoted(event: ChatMemberUpdated) -> None:
    chat_id = event.chat.id
    chat_title = event.chat.title or "Без названия"

    # db.add_channel(chat_id, chat_title)
    logger.info(f"Bot promoted to admin in channel: {chat_title} (ID: {chat_id})")
    try:
        await bot.send_message(
            event.from_user.id, f"Бот стал администратором в канале: {chat_title}"
        )
    except Exception as e:
        logger.error(f"Failed to send message to user {event.from_user.id}: {e}")


# @dp.message_handler(commands=("list_channels",))
# async def list_channels(message: types.Message) -> None:
#     channels = db.get_channels()
#
#     if channels:
#         response = "Список каналов, где я администратор:\n"
#         for chat_id, chat_title in channels:
#             response += f"- {chat_title} (ID: {chat_id})\n"
#     else:
#         response = "Я пока не администратор ни в одном канале."
#
#     await message.answer(response)
#     bot_logger.info(f"User {get_username(message)} requested channel list")
