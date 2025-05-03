from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from loguru import logger

from bot.callbacks import SelectChannelCallback
from bot.callbacks.post import PostActionEnum, PostCallback
from bot.handlers.menu import show_main_menu
from bot.keyboards.inline.post import select_another_channel_keyboard
from bot.schemas import PostContext
from bot.states import PostState
from bot.utils.messages import get_message, make_linked
from bot.utils.user import get_username


__all__ = [
    "router",
]


router = Router(name="wait_text")


@router.callback_query(SelectChannelCallback.filter(), PostState.waiting_for_channel)
async def handle_wait_text(query: CallbackQuery, callback_data: SelectChannelCallback, state: FSMContext) -> None:
    """Обработчик для получения поста, который необходимо создать на канале"""
    selected_channel_title = callback_data.channel_title
    selected_channel_username = callback_data.channel_username

    logger.debug(f'Waiting text for channel "{selected_channel_title}" from {get_username(query)}')

    await state.update_data(
        PostContext(
            selected_channel_title=selected_channel_title,
            selected_channel_username=selected_channel_username,
        ).model_dump()
    )
    await state.set_state(PostState.waiting_for_post)

    linked_channel = make_linked(selected_channel_title, selected_channel_username)
    message_text = f"Вы выбрали канал: {linked_channel}.\n\nТеперь отправьте мне текст для публикации."

    message = await get_message(query)
    await message.edit_text(
        message_text,
        reply_markup=select_another_channel_keyboard(),
        parse_mode="HTML",
    )


# noinspection PyTypeChecker
@router.callback_query(PostCallback.filter(F.action == PostActionEnum.BACK))
async def handle_select_another_channel_callback(query: CallbackQuery, state: FSMContext) -> None:
    """Обработчик для выбора другого канала"""
    logger.debug(f"[handle_back_callback] callback from {get_username(query)}")

    message = await get_message(query)
    await show_main_menu(message, edit_previous_text=True)
    await state.clear()
