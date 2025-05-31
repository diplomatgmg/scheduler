from aiogram import F, Router
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from loguru import logger

from bot.callbacks.post import PostCreateActionEnum, PostCreateCallback
from bot.core.loader import bot
from bot.keyboards.inline.post import post_cancel_buttons
from bot.states.post import PostCreateState
from bot.utils.messages import get_message
from bot.utils.user import get_username


__all__ = ["router"]


router = Router(name="request_buttons")


BUTTONS_FORMAT_TEXT = """
<b>Пришлите URL-кнопки.</b>\n
Пример формата для кнопок в один ряд:
<pre>Кнопка 1 - https://site1.com
Кнопка 2 - https://site2.com</pre>

Пример формата для кнопок в несколько рядов:
<pre>Кнопка 1 - https://site1.com | Кнопка 2 - https://site2.com
Кнопка 3 - https://site3.com | Кнопка 4 - https://site4.com</pre>
"""


# noinspection PyTypeChecker
@router.callback_query(PostCreateCallback.filter(F.action == PostCreateActionEnum.ADD_BUTTONS))
async def request_buttons(query: CallbackQuery, state: FSMContext) -> None:
    """Запрашивает кнопки для поста в необходимом формате."""
    logger.debug(f"{query.data} callback from {get_username(query)}")

    message = await get_message(query)
    await message.delete()

    await bot.send_message(
        text=BUTTONS_FORMAT_TEXT,
        chat_id=message.chat.id,
        reply_markup=post_cancel_buttons(),
        parse_mode=ParseMode.HTML,
    )
    await state.set_state(PostCreateState.process_buttons)
