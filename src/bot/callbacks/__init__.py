from aiogram import Dispatcher
from loguru import logger

from bot.callbacks import menu

__all__ = ["register_callbacks_routers"]


def register_callbacks_routers(dp: Dispatcher) -> None:
    logger.debug("Registering callback routers")

    dp.include_routers(
        menu.router,
    )
