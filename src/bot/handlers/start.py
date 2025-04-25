from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from loguru import logger

from bot.keyboards.inline.menu import main_keyboard
from bot.states.post import PostState
from bot.utils.user import get_username

__all__ = ()

router = Router(name="start")


@router.message(CommandStart())
async def handle_start(message: Message, state: FSMContext) -> None:
    logger.debug(f"Handler start. User: {get_username(message)}")

    message_text = "ТЕСТ. Здесь вы можете создавать посты, просматривать статистику и выполнять другие задачи."
    await message.answer(message_text, reply_markup=main_keyboard())
    await state.set_state(PostState.waiting_for_post)


@router.message(PostState.waiting_for_post)
async def process_post(message: Message, state: FSMContext) -> None:
    logger.debug(f"process handler. User: {get_username(message)}")

    await message.forward(chat_id=message.chat.id)
    await state.clear()
