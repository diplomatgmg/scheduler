from aiogram import Bot, Dispatcher

from bot.core import config

__all__ = [
    "bot",
    "dp",
]

dp = Dispatcher()
bot = Bot(token=config.BOT.token)
