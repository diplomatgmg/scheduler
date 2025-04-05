from aiogram import Dispatcher
from loguru import logger

from bot.handlers import admin_channels, start, test


def register_handlers_routers(dp: Dispatcher) -> None:
    logger.debug("Регистрация handlers routers")

    dp.include_routers(
        start.router,
        test.router,
        admin_channels.router,
    )
