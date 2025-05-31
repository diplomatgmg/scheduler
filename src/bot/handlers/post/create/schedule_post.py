from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from loguru import logger

from bot.callbacks import PostCallback
from bot.callbacks.post import PostActionEnum
from bot.core.loader import bot
from bot.keyboards.inline.post import post_schedule_keyboard
from bot.states import PostCreateState
from bot.utils.messages import get_message
from bot.utils.user import get_username


__all__ = [
    "router",
]


router = Router(name="schedule_post")


# noinspection PyTypeChecker
@router.callback_query(PostCallback.filter(F.action == PostActionEnum.SCHEDULE_POST))
async def handle_schedule_post(query: CallbackQuery, state: FSMContext) -> None:
    """Обрабатывает полученный текст для публикации."""
    logger.debug(f"Schedule post callback from {get_username(query)}")

    message = await get_message(query)

    await message.delete()
    await bot.send_message(
        text="Выберите необходимое действие", chat_id=message.chat.id, reply_markup=post_schedule_keyboard()
    )
    await state.set_state(PostCreateState.waiting_for_buttons)
