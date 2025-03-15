from aiogram import Bot, Dispatcher

from bot.core.config import settings

dp = Dispatcher()
bot = Bot(token=settings.BOT_TOKEN)
