from enum import StrEnum

from aiogram import Router, F
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from loguru import logger

from bot.utils.user import get_username

__all__ = ()

router = Router(name="menu")


class MenuActionEnum(StrEnum):
    CREATE = "create"
    SETTINGS = "settings"
    EDIT = "edit"


class MenuCallback(CallbackData, prefix="menu"):
    action: MenuActionEnum


@router.callback_query(MenuCallback.filter(F.action == MenuActionEnum.CREATE.value))
async def handle_create_callback(
    query: CallbackQuery,
    state: FSMContext,
) -> None:
    logger.debug(f"[CREATE] callback from {get_username(query)}")
    await query.answer("Создание поста")
    await state.clear()


@router.callback_query(MenuCallback.filter(F.action == MenuActionEnum.SETTINGS.value))
async def handle_settings_callback(
    query: CallbackQuery,
    state: FSMContext,
) -> None:
    logger.debug(f"[SETTINGS] callback from {get_username(query)}")
    await query.answer("Настройки открыты")
    await state.clear()


@router.callback_query(MenuCallback.filter(F.action == MenuActionEnum.EDIT.value))
async def handle_edit_callback(
    query: CallbackQuery,
    state: FSMContext,
) -> None:
    logger.debug(f"[EDIT] callback from {get_username(query)}")
    await query.answer("Режим редактирования")
    await state.clear()
