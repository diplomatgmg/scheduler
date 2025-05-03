from aiogram.exceptions import TelegramAPIError
from aiogram.types import CallbackQuery


__all__ = [
    "safe_reply",
]


async def safe_reply(
    query: CallbackQuery,
    text: str,
) -> None:
    """Безопасно отвечает на CallbackQuery."""

    if query.message is not None:
        try:
            await query.message.answer(text)
        except TelegramAPIError:
            await query.answer(text, show_alert=True)
    else:
        await query.answer(text, show_alert=True)
