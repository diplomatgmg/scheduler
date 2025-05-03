from aiogram.types import Message
from loguru import logger

from bot.keyboards.inline.menu import main_keyboard
from bot.utils.user import get_username

__all__ = [
    "show_main_menu",
]


async def show_main_menu(message: Message, *, edit_previous_text: bool = False) -> None:
    logger.debug(f"Showing main menu for user: {get_username(message)}")

    message_text = "Здесь вы можете создавать посты, просматривать статистику и выполнять другие задачи."

    if edit_previous_text:
        await message.edit_text(message_text, reply_markup=main_keyboard())
        return

    await message.answer(message_text, reply_markup=main_keyboard())
