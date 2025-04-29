from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from loguru import logger

from bot.handlers.menu import show_main_menu
from bot.states.post import PostState
from bot.utils.user import get_username

__all__ = [
    "handle_start",
]

router = Router(name="start")


@router.message(CommandStart())
async def handle_start(message: Message) -> None:
    await show_main_menu(message)


# FIXME unused? remove?
@router.message(PostState.waiting_for_post)
async def process_post(message: Message, state: FSMContext) -> None:
    logger.debug(f"process handler. User: {get_username(message)}")

    await message.forward(chat_id=message.chat.id)
    await state.clear()
