from aiogram import Dispatcher
from loguru import logger

from bot.handlers import admin_channels, echo, start, test

__all__ = [
    "register_handlers_routers",
]


def register_handlers_routers(dp: Dispatcher) -> None:
    logger.debug("Registering handler routers")

    dp.include_routers(
        start.router,
        test.router,
        admin_channels.router,
        echo.router,
    )
