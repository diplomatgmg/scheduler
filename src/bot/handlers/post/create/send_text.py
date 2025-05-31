from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.inline.post import post_additional_configuration_keyboard
from bot.schemas import PostContext
from bot.schemas.post import PreviewMessageContext
from bot.states import PostCreateState
from bot.utils.messages import make_linked
from bot.utils.user import get_username
from common.database.models import DelayedMessageModel
from common.database.services.delayed_messages import save_delayed_message


__all__ = [
    "router",
]


router = Router(name="send_text")


@router.message(PostCreateState.waiting_for_post)
async def handle_send_text(message: Message, state: FSMContext, session: AsyncSession) -> None:
    """Обрабатывает полученный текст для публикации."""
    logger.debug(f"Sending text callback from {get_username(message)}")

    post_state = PostContext(**(await state.get_data()))
    post_state.preview_message = PreviewMessageContext(message=message)
    make_linked(post_state.selected_channel_title, post_state.selected_channel_username)

    message_data = message.model_dump(exclude_none=True, exclude_defaults=True)
    delayed_message_model = DelayedMessageModel(
        to_chat_id=post_state.selected_channel_chat_id,
        message_json=message_data,
    )

    await save_delayed_message(session, delayed_message_model)

    await message.send_copy(
        chat_id=message.chat.id,
        reply_markup=post_additional_configuration_keyboard(saved_buttons=post_state.preview_message.buttons),
    )
    await state.set_state(PostCreateState.waiting_for_post)
    await state.set_data(post_state.model_dump())
