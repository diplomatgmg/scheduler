from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from bot.callbacks import PostCallback
from bot.callbacks.post import PostActionEnum
from bot.keyboards.inline.post import select_channel_keyboard
from bot.states import PostState
from bot.utils.messages import get_message, safe_reply
from bot.utils.user import get_username
from common.database.services.user import find_user_channels


__all__ = [
    "router",
]


router = Router(name="select_channel")


# noinspection PyTypeChecker
@router.callback_query(PostCallback.filter(F.action == PostActionEnum.CREATE))
async def handle_select_channel_callback(query: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    """Обработчик для выбора канала, в котором необходимо создать пост"""
    logger.debug(f"Selecting channel callback from {get_username(query)}")

    channels = await find_user_channels(session, query.from_user.id)
    if not channels:
        await safe_reply(query, "Бот не является администратором ни одного канала.")
        return

    await state.clear()
    await state.set_state(PostState.waiting_for_channel)

    message = await get_message(query)
    await message.edit_text(
        text="Выберите канал для публикации поста.",
        reply_markup=select_channel_keyboard(channels),
    )
