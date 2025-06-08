from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram_calendar import SimpleCalendarCallback
from loguru import logger

from bot.callbacks.post import PostScheduleActionEnum, PostScheduleCallback
from bot.handlers.post.schedule.utils import CustomCalendar
from bot.states.post import PostScheduleState
from bot.utils.messages import get_message
from bot.utils.user import get_username


__all__ = [
    "router",
]


router = Router(name="schedule")


# noinspection PyTypeChecker
@router.callback_query(PostScheduleCallback.filter(F.action == PostScheduleActionEnum.SCHEDULE))
async def handle_schedule_post(query: CallbackQuery, state: FSMContext) -> None:
    """Выкладывает пост в определенное время."""
    logger.debug(f"Handle schedule post callback from {get_username(query)}")

    message = await get_message(query)

    reply_markup = await CustomCalendar(locale="ru").start_calendar()
    await message.edit_text("Выберите время для публикации (тест)", reply_markup=reply_markup)
    await state.set_state(PostScheduleState.waiting_for_date)


@router.callback_query(SimpleCalendarCallback.filter(), PostScheduleState.waiting_for_date)
async def process_date_selection(query: CallbackQuery, callback_data: SimpleCalendarCallback) -> None:
    logger.debug(f"Process date selection handler from user {get_username(query)}")

    _, date = await CustomCalendar().process_selection(query, callback_data)

    message = await get_message(query)

    await message.answer(
        f"📅 Выбрана дата: {date}\n⏰ Введите время в формате HH:MM (например, 14:30)"
    )

    # post_schedule_context = PostScheduleContext(date=date.timestamp())  # noqa: ERA001
    # await state.update_data(post_schedule_context.model_dump())  # noqa: ERA001
    # # await state.set_state(PostScheduleState.waiting_for_time)  # noqa: ERA001
