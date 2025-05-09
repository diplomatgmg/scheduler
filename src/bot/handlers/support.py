from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from loguru import logger

from bot.core.config import bot_config
from bot.utils.user import get_username


__all__ = ()

router = Router(name="support")


@router.message(Command("support"))
async def handle_support(message: Message) -> None:
    logger.debug(f"Support handler for user: {get_username(message)}")

    await message.reply(f"Вопросы, предложения, обратная связь - @{bot_config.support_username}")
