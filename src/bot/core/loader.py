from aiogram import Bot, Dispatcher

from src.bot.core.config import settings

dp = Dispatcher()
bot = Bot(token=settings.BOT_TOKEN)
