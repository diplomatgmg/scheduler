from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from loguru import logger

from bot.handlers.menu import show_main_menu
from bot.schemas.menu import MenuActionEnum, MenuCallback
from bot.states.post import PostState
from bot.utils.messages import get_message
from bot.utils.user import get_username

__all__ = [
    "back_router",
]


back_router = Router(name="back")


# noinspection PyTypeChecker
@back_router.callback_query(MenuCallback.filter(F.action == MenuActionEnum.BACK), PostState.waiting_for_channel)
async def handle_back_callback(query: CallbackQuery, state: FSMContext) -> None:
    logger.debug(f"[handle_back_callback] callback from {get_username(query)}")

    await state.clear()

    message = await get_message(query)
    await show_main_menu(message, edit_previous_text=True)
