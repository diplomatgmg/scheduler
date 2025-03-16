from aiogram import Dispatcher
from loguru import logger

from bot.middlewares.database import DatabaseMiddleware


def register_middlewares(dp: Dispatcher) -> None:
    logger.debug("Регистрация middlewares")
    dp.update.outer_middleware(DatabaseMiddleware())
