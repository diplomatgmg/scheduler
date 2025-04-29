from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from loguru import logger

from bot.callbacks.utils import make_linked
from bot.states.post import PostState
from bot.utils.user import get_username

__all__ = [
    "send_text_router",
]


send_text_router = Router(name="send_text")


@send_text_router.message(PostState.waiting_for_text, F.text)
async def handle_send_text(message: Message, state: FSMContext) -> None:
    """Обрабатывает полученный текст для публикации."""
    logger.debug(f"[handle_send_text] Received text from {get_username(message)}")

    user_data = await state.get_data()

    # FIXME. Немного не понял.
    #  До этого использовал callback_data, а тут обращение по ключу.
    selected_channel_title = user_data.get("selected_channel_title")
    selected_channel_username = user_data.get("selected_channel_username")

    if not selected_channel_title or not selected_channel_username:
        await message.answer("Произошла внутренняя ошибка. Перезапустите бота.")
        logger.critical(f"State: {state}. Message {message}")
        return

    # FIXME ????????
    make_linked(selected_channel_title, selected_channel_username)

    # FIXME Понять в каких ситуациях это происходит
    if not selected_channel_title:
        logger.error(f"No selected channel found in state for user {get_username(message)}")
        await message.reply("Произошла ошибка. Пожалуйста, попробуйте начать создание поста сначала.")
        await state.clear()
        return

    post_text = message.text

    # FIXME Сделать linked
    await message.answer(
        f"Получен текст для публикации в канал {selected_channel_title}:\n\n"
        f"{post_text}\n\n"
        "Функция публикации пока не реализована. Состояние FSM сброшено."
    )

    # FIXME Пока не до конца понял, в каких ситуациях необходимо сбрасывать состояния
    await state.clear()
