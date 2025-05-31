from aiogram import F, Router
from aiogram.types import CallbackQuery
from loguru import logger

from bot.callbacks.post import PostScheduleActionEnum, PostScheduleCallback
from bot.utils.messages import get_message
from bot.utils.user import get_username


__all__ = ["router"]


router = Router(name="set_delete_timer")


# noinspection PyTypeChecker
@router.callback_query(PostScheduleCallback.filter(F.action == PostScheduleActionEnum.SET_DELETE_TIMER))
async def handle_set_delete_timer_post(query: CallbackQuery) -> None:
    """Выкладывает пост в определенное время."""
    logger.debug(f"Handle set delete timer post callback from {get_username(query)}")

    message = await get_message(query)
    await message.edit_text("Через какое время необходимо удалить пост? (тест)")
