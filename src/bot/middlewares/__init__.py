from aiogram import Dispatcher
from loguru import logger

from bot.middlewares.auth import AuthMiddleware
from bot.middlewares.database import DatabaseMiddleware

__all__ = [
    "register_middlewares",
]


def register_middlewares(dp: Dispatcher) -> None:
    logger.debug("Register middlewares")

    dp.update.outer_middleware(DatabaseMiddleware())
    dp.message.outer_middleware(AuthMiddleware())
