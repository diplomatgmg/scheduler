from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.callbacks.location import LocationActionEnum, LocationCallback
from bot.keyboards.inline.location import (
    timezone_offset_selection_keyboard,
)
from bot.states.location import LocationState
from bot.utils.messages import get_message


__all__ = ["router"]


router = Router(name="offset_selection")


def get_utc_offsets() -> list[int]:
    """Получаем смещения UTC в формате: -12, -11, ..., 11, 12"""
    return list(range(-12, 13))


# noinspection PyTypeChecker
@router.callback_query(
    LocationCallback.filter(F.action == LocationActionEnum.CHOOSE_LOCATION), LocationState.waiting_for_method
)
async def process_offset_selection(query: CallbackQuery, state: FSMContext) -> None:
    message = await get_message(query)

    offsets = get_utc_offsets()

    await message.edit_text(
        "Выберите временную зону относительно UTC.\n\n"
        '<a href="https://time.is/your_time_zone">Какая у меня временная зона?</a>',
        reply_markup=timezone_offset_selection_keyboard(offsets),
        disable_web_page_preview=True,
        parse_mode=ParseMode.HTML,
    )
    await state.set_state(LocationState.waiting_for_manual_choose)
