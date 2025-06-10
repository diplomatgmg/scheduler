from typing import cast

from aiogram import F, Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.callbacks.location import LocationCallback
from bot.handlers.location.utils import update_user_offset
from bot.states.location import LocationState
from bot.utils.messages import get_message
from common.database.models import UserModel


__all__ = ["router"]


router = Router(name="offset_selected")


# noinspection PyTypeChecker
@router.callback_query(LocationCallback.filter(F.offset.is_not(None)), LocationState.waiting_for_manual_choose)
async def handle_offset_selected(
    query: CallbackQuery, callback_data: LocationCallback, session: AsyncSession, user: UserModel
) -> None:
    message = await get_message(query)
    offset = cast("int", callback_data.offset)

    await update_user_offset(message, session, user, offset, edit_message=True)
