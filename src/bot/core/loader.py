from aiogram import Bot, Dispatcher

from bot.core.config import bot_config


__all__ = [
    "bot",
    "dp",
]


dp = Dispatcher()
bot = Bot(token=bot_config.token)
