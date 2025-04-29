from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from loguru import logger

from bot.callbacks.utils import make_linked
from bot.keyboards.inline.menu import select_another_channel_keyboard
from bot.schemas.menu import ChannelSelectCallback
from bot.states.post import PostState
from bot.utils.messages import get_message
from bot.utils.user import get_username

__all__ = [
    "wait_text_router",
]


wait_text_router = Router(name="wait_text")


@wait_text_router.callback_query(ChannelSelectCallback.filter(), PostState.waiting_for_channel)
async def handle_channel_selected(
    query: CallbackQuery, callback_data: ChannelSelectCallback, state: FSMContext
) -> None:
    selected_channel_title = callback_data.channel_title
    selected_channel_username = callback_data.channel_username

    logger.debug(f"[handle_channel_selected] Channel '{selected_channel_title}' selected by {get_username(query)}")

    # TODO Изучить подробнее строчки ниже. Позже они используются в handle_send_text в user_data.get()
    await state.update_data(
        selected_channel_title=selected_channel_title, selected_channel_username=selected_channel_username
    )
    await state.set_state(PostState.waiting_for_text)

    linked_channel = make_linked(selected_channel_title, selected_channel_username)
    message_text = f"Вы выбрали канал: {linked_channel}.\n\nТеперь отправьте мне текст для публикации."

    message = await get_message(query)
    await message.edit_text(
        message_text,
        reply_markup=select_another_channel_keyboard(),
        parse_mode="HTML",
    )
