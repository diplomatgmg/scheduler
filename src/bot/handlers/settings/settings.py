from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from loguru import logger

from bot.callbacks.post import PostMenuActionEnum, PostMenuCallback
from bot.utils.messages import get_message
from bot.utils.user import get_username


__all__ = [
    "router",
]


router = Router(name="settings")


# noinspection PyTypeChecker
@router.callback_query(PostMenuCallback.filter(F.action == PostMenuActionEnum.SETTINGS))
async def handle_settings_callback(
    query: CallbackQuery,
    state: FSMContext,
) -> None:
    logger.debug(f"Settings callback from {get_username(query)}")

    message = await get_message(query)
    await message.answer("Настройки открыты")
    await state.clear()
