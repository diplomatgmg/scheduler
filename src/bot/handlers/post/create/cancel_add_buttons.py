from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from loguru import logger

from bot.callbacks import PostCallback
from bot.callbacks.post import PostActionEnum
from bot.keyboards.inline.post import post_additional_configuration
from bot.schemas import PostContext
from bot.states import PostState
from bot.utils.messages import get_message
from bot.utils.user import get_username


__all__ = [
    "router",
]


router = Router(name="add_buttons")


# noinspection PyTypeChecker
@router.callback_query(PostCallback.filter(F.action == PostActionEnum.CANCEL_ADD_BUTTONS))
async def handle_cancel_add_buttons(query: CallbackQuery, state: FSMContext) -> None:
    """Обрабатывает отмену добавления кнопок и возвращает предпросмотр сообщения."""
    logger.debug(f"Cancel add buttons callback from {get_username(query)}")

    message = await get_message(query)

    post_state_data = await state.get_data()
    post_context = PostContext(**post_state_data)

    if post_context.preview_message is None or post_context.preview_message.text is None:
        logger.error(f"Preview message/message text is empty.\npreview_message={post_context.preview_message}")
        await message.answer("Не удалось отменить создание кнопок")
        return

    await message.edit_text(post_context.preview_message.text, reply_markup=post_additional_configuration())

    await state.set_state(PostState.waiting_for_post)
