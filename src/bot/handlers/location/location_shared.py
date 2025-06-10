from datetime import datetime

from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardRemove
import pytz  # type: ignore[import-untyped]
from sqlalchemy.ext.asyncio import AsyncSession
from timezonefinder import TimezoneFinder

from bot.handlers.location.utils import update_user_offset
from bot.states.location import LocationState
from bot.utils.user import get_user


__all__ = ["router"]


router = Router(name="location")


# noinspection PyTypeChecker
@router.message(LocationState.waiting_for_share, F.location)
async def handle_location_shared(message: Message, session: AsyncSession) -> None:
    latitude, longitude = message.location.latitude, message.location.longitude  # type: ignore[union-attr]
    tf = TimezoneFinder()

    timezone_str = tf.timezone_at(lat=latitude, lng=longitude)
    if timezone_str is None:
        await message.answer(
            "Не удалось определить временную зону. Пожалуйста, попробуйте еще раз или выберите вручную.",
            reply_markup=ReplyKeyboardRemove(),
        )
    tz = pytz.timezone(timezone_str)
    offset = tz.utcoffset(datetime.now()).total_seconds() / 3600

    user = await get_user(message)

    await update_user_offset(message, session, user.id, offset)
