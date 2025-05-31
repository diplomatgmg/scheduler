from aiogram import F, Router
from aiogram.types import CallbackQuery
from loguru import logger

from bot.callbacks.post import PostScheduleActionEnum, PostScheduleCallback
from bot.utils.messages import get_message
from bot.utils.user import get_username


__all__ = [
    "router",
]


router = Router(name="schedule")


# noinspection PyTypeChecker
@router.callback_query(PostScheduleCallback.filter(F.action == PostScheduleActionEnum.SCHEDULE))
async def handle_schedule_post(query: CallbackQuery) -> None:
    """Выкладывает пост в определенное время."""
    logger.debug(f"Handle schedule post callback from {get_username(query)}")

    message = await get_message(query)
    await message.edit_text("Выберите время для публикации (тест)")
