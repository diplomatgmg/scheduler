from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from loguru import logger

from bot.schemas import PostContext
from bot.states import PostState
from bot.utils.messages import make_linked
from bot.utils.user import get_username

__all__ = [
    "router",
]


router = Router(name="send_text")


# FIXME Работает только с текстом. Не умеет работать с фото/видео/аудио и т.п.
@router.message(PostState.waiting_for_post)
async def handle_send_text(message: Message, state: FSMContext) -> None:
    """Обрабатывает полученный текст для публикации."""
    logger.debug(f"[handle_send_text] Received text from {get_username(message)}")

    post_state = PostContext(**(await state.get_data()))
    linked_channel = make_linked(post_state.selected_channel_title, post_state.selected_channel_username)

    await message.answer(
        f"Получен текст для публикации в канал {linked_channel}:\n\n"
        f"{message.text}\n\n"
        "Функция публикации пока не реализована. Состояние FSM сброшено.",
        parse_mode="HTML",
    )

    # FIXME Пока не до конца понял, в каких ситуациях необходимо сбрасывать состояния
    await state.clear()
