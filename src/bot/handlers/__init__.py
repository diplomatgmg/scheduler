from aiogram import Dispatcher
from loguru import logger

from bot.handlers import admin_channels, post, start, support, unhandled_message


__all__ = [
    "register_handlers_routers",
]


def register_handlers_routers(dp: Dispatcher) -> None:
    logger.debug("Registering handler routers")

    dp.include_routers(
        support.router,
        start.router,
        admin_channels.router,
        post.router,
        # always bottom
        unhandled_message.router,
    )
