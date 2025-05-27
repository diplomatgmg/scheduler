from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.handlers.menu import show_main_menu
from bot.states import PostState


__all__ = [
    "handle_start",
]

router = Router(name="start")


@router.message(CommandStart())
async def handle_start(message: Message, state: FSMContext) -> None:
    await show_main_menu(message)
    await state.set_state(PostState.waiting_for_buttons)
