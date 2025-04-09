from enum import StrEnum

from aiogram import Router
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from loguru import logger

from bot.utils.user import get_username

__all__ = [
    "MenuActionEnum",
    "MenuCallback",
    "handle_menu_callback",
]

router = Router(name="menu")


class MenuActionEnum(StrEnum):
    SETTINGS = "settings"


class MenuCallback(CallbackData, prefix="menu"):
    action: MenuActionEnum


@router.callback_query(MenuCallback.filter())
async def handle_menu_callback(
    query: CallbackQuery,
    callback_data: MenuCallback,
    state: FSMContext,
) -> None:
    logger.debug(f"callback: {callback_data.action} from {get_username(query)}")

    if callback_data.action == MenuActionEnum.SETTINGS:
        await query.answer("Ты открыл настройки!")

    await query.answer()
    await state.clear()
