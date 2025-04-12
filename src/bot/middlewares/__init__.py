from aiogram import Dispatcher
from loguru import logger

from bot.core import settings
from bot.middlewares.auth import AuthMiddleware
from bot.middlewares.database import DatabaseMiddleware
from bot.middlewares.logging import LoggingMiddleware

__all__ = [
    "register_middlewares",
]


def register_middlewares(dp: Dispatcher) -> None:
    logger.debug("Register middlewares")

    if settings.debug:
        dp.update.outer_middleware(LoggingMiddleware())

    dp.update.outer_middleware(DatabaseMiddleware())
    dp.message.outer_middleware(AuthMiddleware())
