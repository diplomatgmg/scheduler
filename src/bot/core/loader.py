from aiogram import Bot, Dispatcher

from bot.core import settings

dp = Dispatcher()
bot = Bot(token=settings.BOT.token)
