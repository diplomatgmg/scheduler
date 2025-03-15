from enum import Enum

from aiogram import Router
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from loguru import logger

router = Router(name="menu")


class MenuActionEnum(str, Enum):
    SETTINGS = "settings"


class MenuCallback(CallbackData, prefix="menu"):
    action: MenuActionEnum


@router.callback_query(MenuCallback.filter())
async def handle_menu_callback(
    query: CallbackQuery,
    callback_data: MenuCallback,
    state: FSMContext,
) -> None:
    logger.debug(
        f"Получен callback: {callback_data.action} от @{query.from_user.username}"
    )
    if callback_data.action == MenuActionEnum.SETTINGS:
        await query.message.answer("Ты открыл настройки!")
    await query.answer()
    await state.clear()
