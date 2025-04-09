from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from loguru import logger

from bot.utils.user import get_username

__all__ = ()

router = Router(name="test")


@router.message(Command(commands=("test",)))
async def handle_test(message: Message) -> None:
    logger.debug(f"Handler test. User: {get_username(message)}")

    await message.answer("test :)")
