from aiogram import Bot, Dispatcher

from bot.core import settings

__all__ = [
    "bot",
    "dp",
]

dp = Dispatcher()
bot = Bot(token=settings.BOT.token)
