from aiogram import Dispatcher
from loguru import logger

from bot.handlers import start
from bot.handlers import test


def register_handlers_routers(dp: Dispatcher) -> None:
    logger.debug("Регистрация handlers routers")

    dp.include_routers(
        start.router,
        test.router,
    )
