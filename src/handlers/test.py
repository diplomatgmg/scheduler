from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router(name="test")


@router.message(Command(commands=("test",)))
async def handle_test(message: Message) -> None:
    await message.answer(f"test :)")
