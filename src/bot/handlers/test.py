from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import Router
from aiogram.filters import Command

if TYPE_CHECKING:
    from aiogram.types import Message

router = Router(name="test")


@router.message(Command(commands=("test",)))
async def handle_test(message: Message) -> None:
    await message.answer("test :)")
