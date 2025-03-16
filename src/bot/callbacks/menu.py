from enum import Enum

from aiogram import Router
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from loguru import logger

from bot.utils import get_username

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
    logger.debug(f"Получен callback: {callback_data.action} от {get_username(query)}")

    if callback_data.action == MenuActionEnum.SETTINGS:
        if query.message is not None:
            await query.message.answer("Ты открыл настройки!")
        else:
            logger.error(f"Сообщение недоступно для callback от {get_username(query)}")

    await query.answer()
    await state.clear()
