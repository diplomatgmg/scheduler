from aiogram.exceptions import TelegramAPIError
from aiogram.types import CallbackQuery

from typing import ParamSpecKwargs
__all__ = [
    "safe_reply",
]

async def save_edit(
        query: CallbackQuery,
        text: str,
) -> None:
    """Безопасно отвечает на CallbackQuery."""

    try:
        await bot.edit_message_text()

    if query.message is not None:
        try:
            await query.message.answer(text)
        except TelegramAPIError:
            await query.answer(text, show_alert=True)
    else:
        await query.answer(text, show_alert=True)



# await bot.edit_message_text(
#     text=BUTTONS_FORMAT_TEXT,
#     chat_id=message.chat.id,
#     message_id=message.message_id,
#     reply_markup=post_cancel_buttons(),
#     parse_mode=ParseMode.HTML,
# )