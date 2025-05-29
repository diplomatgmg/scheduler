from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from loguru import logger

from bot.callbacks import PostCallback
from bot.callbacks.post import PostActionEnum
from bot.core.loader import bot
from bot.keyboards.inline.post import post_additional_configuration
from bot.schemas import PostContext
from bot.states import PostState
from bot.utils.messages import get_message
from bot.utils.user import get_username


__all__ = [
    "router",
]


router = Router(name="remove_buttons")


# noinspection PyTypeChecker
@router.callback_query(PostCallback.filter(F.action == PostActionEnum.REMOVE_BUTTONS))
async def handle_remove_add_buttons(query: CallbackQuery, state: FSMContext) -> None:
    """Удаляет кнопки и возвращает предпросмотр сообщения."""
    logger.debug(f"Remove buttons callback from {get_username(query)}")

    message = await get_message(query)

    post_state_data = await state.get_data()
    post_context = PostContext(**post_state_data)

    if post_context.preview_message is None:
        logger.error(f"Preview message is empty.\npreview_message={post_context.preview_message}")
        await message.answer("Не удалось отменить создание кнопок")
        return

    await message.delete()
    await bot.copy_message(
        chat_id=message.chat.id,
        from_chat_id=post_context.preview_message.message.chat.id,
        message_id=post_context.preview_message.message.message_id,
        reply_markup=post_additional_configuration(),
    )

    await state.set_state(PostState.waiting_for_post)
