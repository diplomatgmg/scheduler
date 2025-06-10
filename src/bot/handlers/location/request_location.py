from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.keyboards.commands.enums import DefaultCommandEnum
from bot.keyboards.inline.location import (
    location_selection_keyboard,
)
from bot.states.location import LocationState


__all__ = ["router"]


router = Router(name="request_location")


@router.message(Command(DefaultCommandEnum.SET_TIMEZONE))
@router.message(LocationState.waiting_for_method)
async def request_location(message: Message) -> None:
    """Отправляет запрос на установку временной зоны"""
    await message.answer(
        "Каким способом вы хотите изменить временную зону?",
        reply_markup=location_selection_keyboard(),
    )
