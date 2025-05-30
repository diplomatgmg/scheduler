from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.handlers.menu import show_main_menu


__all__ = ()


router = Router(name="start")


@router.message(CommandStart())
async def handle_start(message: Message) -> None:
    await show_main_menu(message)
