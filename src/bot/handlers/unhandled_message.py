from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from loguru import logger

from bot.handlers.menu import show_main_menu
from bot.utils.messages import get_message
from bot.utils.user import get_username


__all__ = ["router"]


router = Router(name="unhandled_event")


@router.message()
@router.callback_query()
async def unhandled_event(event: Message | CallbackQuery, state: FSMContext) -> None:
    """Обработчик для необработанных сообщений"""
    logger.warning(f"Unhandled message from {get_username(event)}")

    await state.clear()

    message = event if isinstance(event, Message) else await get_message(event)
    await message.delete()

    await show_main_menu(message)
