from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from loguru import logger

from bot.callbacks.post import PostCreateActionEnum, PostCreateCallback
from bot.core.loader import bot
from bot.keyboards.inline.post import scheduling_options_keyboard
from bot.states.post import PostCreateState
from bot.utils.messages import get_message
from bot.utils.user import get_username


__all__ = ["router"]


router = Router(name="open_scheduling_options")


# noinspection PyTypeChecker
@router.callback_query(PostCreateCallback.filter(F.action == PostCreateActionEnum.SCHEDULE))
async def open_scheduling_options(query: CallbackQuery, state: FSMContext) -> None:
    """Показывает меню опций планирования публикации"""
    logger.debug(f"{query.data} callback from {get_username(query)}")

    message = await get_message(query)

    await message.delete()
    await bot.send_message(
        text="Выберите необходимое действие",
        chat_id=message.chat.id,
        reply_markup=scheduling_options_keyboard(),
    )
    await state.set_state(PostCreateState.process_publish)
