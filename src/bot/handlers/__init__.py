from aiogram import Dispatcher
from loguru import logger

from bot.handlers import admin_channels, location, noop, post, start, support


__all__ = [
    "register_handlers_routers",
]


def register_handlers_routers(dp: Dispatcher) -> None:
    logger.debug("Registering handler routers")

    dp.include_routers(
        location.router,
        start.router,
        support.router,
        admin_channels.router,
        post.router,
        noop.router,
    )
