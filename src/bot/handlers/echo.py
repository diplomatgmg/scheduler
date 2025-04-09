from aiogram import Router
from aiogram.types import Message
from loguru import logger

from bot.utils.user import get_username

__all__ = ()

router = Router(name="echo")


@router.message()
async def handle_echo(message: Message) -> None:
    logger.debug(f"Handler echo. User: {get_username(message)}")

    if message.text:
        await message.answer(message.text)
        return
    if message.photo:
        await message.answer_photo(message.photo[0].file_id)
        return
    if message.audio:
        await message.answer_audio(message.audio.file_id)
        return

    logger.error(f"Неизвестный формат сообщения: {message.content_type}")
    await message.answer("Я не понимаю что ты прислал :(")
