from datetime import datetime

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram_calendar import SimpleCalendarCallback  # type: ignore[import-untyped]
from loguru import logger

from bot.callbacks.post import PostScheduleActionEnum, PostScheduleCallback
from bot.handlers.post.schedule.utils import CustomCalendar, parse_time
from bot.schemas.post import PostScheduleContext
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

    reply_markup = await CustomCalendar(locale="ru").start_calendar()  # FIXME locale hardcore
    await message.edit_text("Выберите дату для публикации", reply_markup=reply_markup)
    await state.set_state(PostScheduleState.waiting_for_date)


@router.callback_query(SimpleCalendarCallback.filter(), PostScheduleState.waiting_for_date)
async def process_date_selection(
    query: CallbackQuery, callback_data: SimpleCalendarCallback, state: FSMContext
) -> None:
    logger.debug(f"Process date selection handler from user {get_username(query)}")

    calendar = CustomCalendar(locale="ru")
    selected, processed_date = await calendar.process_selection(query, callback_data)

    if selected:
        post_schedule_context = PostScheduleContext(date=processed_date.timestamp())
        await state.update_data(post_schedule_context.model_dump())

        message = await get_message(query)
        await message.edit_text(
            f"📅 Выбрана дата: {processed_date.strftime('%d.%m.%Y')}\n⏰ Введите время, в удобном для Вас формате"
        )

        await state.set_state(PostScheduleState.waiting_for_time)


@router.message(PostScheduleState.waiting_for_time)
async def process_time_selection(message: Message, state: FSMContext) -> None:
    """Обрабатывает ввод времени пользователем."""
    logger.debug(f"Process time selection handler from user {get_username(message)}")

    parsed_time = parse_time(message.text)
    if parsed_time is None:
        await message.answer("❌ Неверный формат времени. Попробуйте еще раз")
        await state.set_state(PostScheduleState.waiting_for_time)
        return

    user_data = await state.get_data()
    timestamp_date = user_data.get("date")

    if timestamp_date is None:
        await message.answer("❌ Дата не найдена. Попробуйте выбрать дату заново.")
        await state.set_state(PostScheduleState.waiting_for_date)
        return

    date = datetime.fromtimestamp(timestamp_date)
    final_datetime = datetime.combine(date.date(), parsed_time)

    await state.update_data(time=final_datetime.timestamp())
    await message.answer(f"✅ Создана отложенная публикация {final_datetime.strftime('%d.%m.%Y в %H:%M')}")

    # Здесь можешь вызвать финальную функцию планирования или переход к следующему этапу:
    # await plan_post(state) или что-то подобное
    await state.set_state(PostScheduleState.waiting_for_publish)
