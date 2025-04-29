from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.inline.menu import select_channel_keyboard
from bot.schemas.menu import MenuActionEnum, MenuCallback
from bot.services.user import find_user_channels
from bot.states.post import PostState
from bot.utils.messages import get_message, safe_reply
from bot.utils.user import get_username

__all__ = [
    "create_post_router",
]


create_post_router = Router(name="create_post")


# noinspection PyTypeChecker
@create_post_router.callback_query(MenuCallback.filter(F.action == MenuActionEnum.CREATE))
async def handle_select_channel_callback(query: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    logger.debug(f"[handle_select_channel_callback] callback from {get_username(query)}")

    channels = await find_user_channels(session, query.from_user)
    if not channels:
        await safe_reply(query, "Бот не является администратором ни одного канала.")
        return

    await state.clear()
    await state.set_state(PostState.waiting_for_channel)

    message = await get_message(query)
    await message.edit_text(text="Выберите канал для публикации поста.", reply_markup=select_channel_keyboard(channels))
