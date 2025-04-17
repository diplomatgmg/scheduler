from enum import StrEnum

from aiogram import F, Router
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from bot.services.user import find_user_channels
from bot.utils.messages import safe_reply
from bot.utils.user import get_username

__all__ = ()

router = Router(name="menu")


class MenuActionEnum(StrEnum):
    CREATE = "create"
    SETTINGS = "settings"
    EDIT = "edit"


class MenuCallback(CallbackData, prefix="menu"):
    action: MenuActionEnum


class PostStates(StatesGroup):
    waiting_for_channel = State()
    waiting_for_text = State()


# mypy корректно видит тип, ide - нет
# noinspection PyTypeChecker
@router.callback_query(MenuCallback.filter(F.action == MenuActionEnum.CREATE))
async def handle_create_callback(query: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    logger.debug(f"[CREATE] callback from {get_username(query)}")

    channels = await find_user_channels(session, query.from_user)
    if not channels:
        await safe_reply(query, "У вас ещё не добавлены каналы. Добавьте хотя бы один.")
        return

    await state.clear()
    await state.set_state(PostStates.waiting_for_text)


# noinspection PyTypeChecker
@router.callback_query(MenuCallback.filter(F.action == MenuActionEnum.SETTINGS))
async def handle_settings_callback(
    query: CallbackQuery,
    state: FSMContext,
) -> None:
    logger.debug(f"[SETTINGS] callback from {get_username(query)}")
    await query.answer("Настройки открыты")
    await state.clear()


# noinspection PyTypeChecker
@router.callback_query(MenuCallback.filter(F.action == MenuActionEnum.EDIT))
async def handle_edit_callback(
    query: CallbackQuery,
    state: FSMContext,
) -> None:
    logger.debug(f"[EDIT] callback from {get_username(query)}")
    await query.answer("Режим редактирования")
    await state.clear()
