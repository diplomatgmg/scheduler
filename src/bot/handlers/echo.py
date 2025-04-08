from aiogram import Router
from aiogram.types import Message

router = Router(name="echo")


@router.message()
async def handle_echo(message: Message) -> None:
    if message.text is not None:
        await message.answer(message.text)
    else:
        await message.reply("Это не текст :(")
