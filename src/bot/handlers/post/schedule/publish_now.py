from aiogram import F, Router
from aiogram.types import CallbackQuery
from loguru import logger

from bot.callbacks.post import PostScheduleActionEnum, PostScheduleCallback
from bot.utils.messages import get_message
from bot.utils.user import get_username


__all__ = ["router"]


router = Router(name="publish_now")


# noinspection PyTypeChecker
@router.callback_query(PostScheduleCallback.filter(F.action == PostScheduleActionEnum.PUBLISH_NOW))
async def handle_publish_now_post(query: CallbackQuery) -> None:
    """Выкладывает пост прямо сейчас."""
    logger.debug(f"Handle publish now callback from {get_username(query)}")

    message = await get_message(query)
    await message.edit_text("Опубликовано (тест)")
