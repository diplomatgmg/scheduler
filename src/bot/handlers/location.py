from aiogram import Router
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.callbacks.timezone import TimezoneCallback
from bot.keyboards.commands.enums import DefaultCommandEnum
from bot.keyboards.inline.location import timezone_offset_selection_keyboard
from bot.states.location import TimezoneSetupState
from bot.utils.messages import get_message
from bot.utils.user.get_user import get_user
from common.database.services.user.update_user import update_user


router = Router(name="location")


def get_utc_offsets() -> list[int]:
    """Получаем смещения UTC в формате: -12, -11, ..., 11, 12"""
    return list(range(-12, 13))


@router.message(Command(DefaultCommandEnum.SET_TIMEZONE))
@router.message(TimezoneSetupState.waiting_for_timezone)
async def choose_timezone_handler(message: Message) -> None:
    """Обработчик выбора временной зоны по UTC-смещению"""
    offsets = get_utc_offsets()

    await message.answer(
        "Выберите временную зону относительно UTC.\n\n"
        '<a href="https://time.is/your_time_zone">Какая у меня временная зона?</a>',
        reply_markup=timezone_offset_selection_keyboard(offsets),
        disable_web_page_preview=True,
        parse_mode=ParseMode.HTML,
    )


@router.callback_query(TimezoneCallback.filter())
async def handle_zone_selection(
    query: CallbackQuery,
    callback_data: TimezoneCallback,
    session: AsyncSession,
) -> None:
    """Обработчик выбора конкретной временной зоны"""
    message = await get_message(query)
    user = await get_user(query)
    offset = callback_data.offset

    await update_user(session, user.id, timezone_offset=offset)

    formatted_offset = f"UTC{offset}" if offset < 0 else f"UTC+{offset}"
    await message.edit_text(f"✅ Установлена временная зона: {formatted_offset}")
