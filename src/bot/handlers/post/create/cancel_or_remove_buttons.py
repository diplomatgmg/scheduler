from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from loguru import logger

from bot.callbacks import PostCallback
from bot.callbacks.post import PostActionEnum
from bot.core.loader import bot
from bot.keyboards.inline.post import post_additional_configuration_keyboard
from bot.schemas import PostContext
from bot.utils.messages import get_message
from bot.utils.user import get_username


__all__ = [
    "router",
]


router = Router(name="cancel_or_remove_buttons")


# noinspection PyTypeChecker
@router.callback_query(
    PostCallback.filter(
        F.action.in_(
            [
                PostActionEnum.CANCEL_ADD_BUTTONS,
                PostActionEnum.REMOVE_BUTTONS,
            ]
        )
    )
)
async def handle_cancel_or_remove_buttons(query: CallbackQuery, state: FSMContext) -> None:
    logger.debug(f"{query.data} callback from {get_username(query)}")
    message = await get_message(query)
    post_state_data = await state.get_data()
    post_context = PostContext(**post_state_data)

    if post_context.preview_message is None:
        logger.error("Preview message is empty")
        await message.answer("Не удалось отменить создание кнопок")
        return

    await message.delete()
    await bot.copy_message(
        chat_id=message.chat.id,
        from_chat_id=post_context.preview_message.message.chat.id,
        message_id=post_context.preview_message.message.message_id,
        reply_markup=post_additional_configuration_keyboard(),
    )
