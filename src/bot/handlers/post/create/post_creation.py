from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from bot.callbacks.post import PostMenuActionEnum, PostMenuCallback
from bot.keyboards.inline.post import select_channel_keyboard
from bot.states.post import PostCreateState
from bot.utils.messages import get_message, safe_reply
from bot.utils.user import get_username
from common.database.services.user import find_user_channels


__all__ = ["router"]


router = Router(name="post_creation")


# noinspection PyTypeChecker
@router.callback_query(PostMenuCallback.filter(F.action == PostMenuActionEnum.CREATE))
async def post_creation(query: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    """Выбора канала, в котором необходимо создать пост."""
    logger.debug(f"{query.data} callback from {get_username(query)}")

    channels = await find_user_channels(session, query.from_user.id)
    if not channels:
        await safe_reply(query, "Бот не является администратором ни одного канала.")
        return

    message = await get_message(query)
    await message.edit_text(
        text="Выберите канал для публикации поста.",
        reply_markup=select_channel_keyboard(channels),
    )
    await state.set_state(PostCreateState.channel_selection)
