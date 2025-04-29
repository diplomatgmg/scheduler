from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from loguru import logger

from bot.schemas.menu import MenuActionEnum, MenuCallback
from bot.utils.messages import get_message
from bot.utils.user import get_username

__all__ = [
    "edit_router",
]


edit_router = Router(name="edit")


# noinspection PyTypeChecker
@edit_router.callback_query(MenuCallback.filter(F.action == MenuActionEnum.EDIT))
async def handle_edit_callback(
    query: CallbackQuery,
    state: FSMContext,
) -> None:
    logger.debug(f"[handle_edit_callback] callback from {get_username(query)}")

    message = await get_message(query)
    await message.answer("Редактирование открыто")
    await state.clear()
