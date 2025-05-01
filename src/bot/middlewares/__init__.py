from aiogram import Dispatcher
from loguru import logger

from bot.core import config
from bot.middlewares.auth import AuthMiddleware
from bot.middlewares.database import DatabaseMiddleware
from bot.middlewares.logging import LoggingMiddleware
from common.environment.config import env_config

__all__ = [
    "config",
    "register_middlewares",
]


def register_middlewares(dp: Dispatcher) -> None:
    logger.debug("Registering middlewares")

    if env_config.debug:
        dp.update.outer_middleware(LoggingMiddleware())

    dp.update.outer_middleware(DatabaseMiddleware())
    dp.message.outer_middleware(AuthMiddleware())
