from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.callbacks.location import LocationActionEnum, LocationCallback
from bot.keyboards.inline.location import (
    share_location_keyboard,
)
from bot.states.location import LocationState
from bot.utils.messages import get_message


__all__ = ["router"]


router = Router(name="share_location")


# noinspection PyTypeChecker
@router.callback_query(LocationCallback.filter(F.action == LocationActionEnum.SHARE_LOCATION))
async def handle_share_location(query: CallbackQuery, state: FSMContext) -> None:
    message = await get_message(query)

    await message.answer(
        "Пожалуйста, отправьте вашу геолокацию с помощью соответствующей кнопки ниже.",
        reply_markup=share_location_keyboard(),
    )
    await state.set_state(LocationState.waiting_for_share)
