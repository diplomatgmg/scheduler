from aiogram import Bot, Dispatcher

from core import config

dp = Dispatcher()
bot = Bot(token=config.BOT_TOKEN)
