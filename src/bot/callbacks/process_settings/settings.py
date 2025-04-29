from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from loguru import logger

from bot.schemas.menu import MenuActionEnum, MenuCallback
from bot.utils.messages import get_message
from bot.utils.user import get_username

__all__ = [
    "settings_router",
]


settings_router = Router(name="settings")


# noinspection PyTypeChecker
@settings_router.callback_query(MenuCallback.filter(F.action == MenuActionEnum.SETTINGS))
async def handle_settings_callback(
    query: CallbackQuery,
    state: FSMContext,
) -> None:
    logger.debug(f"[handle_settings_callback] callback from {get_username(query)}")

    message = await get_message(query)
    await message.answer("Настройки открыты")
    await state.clear()
