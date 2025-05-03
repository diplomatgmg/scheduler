from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from loguru import logger

from bot.callbacks import PostCallback
from bot.callbacks.post import PostActionEnum
from bot.utils.messages import get_message
from bot.utils.user import get_username


__all__ = [
    "router",
]


router = Router(name="edit")


# noinspection PyTypeChecker
@router.callback_query(PostCallback.filter(F.action == PostActionEnum.EDIT))
async def handle_edit_callback(
    query: CallbackQuery,
    state: FSMContext,
) -> None:
    logger.debug(f"Editing post callback from {get_username(query)}")

    message = await get_message(query)
    await message.answer("Редактирование открыто")
    await state.clear()
