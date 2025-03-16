from aiogram import Dispatcher
from loguru import logger

from bot.callbacks import menu


def register_callbacks_routers(dp: Dispatcher) -> None:
    logger.debug("Регистрация callbacks routers")

    dp.include_routers(
        menu.router
    )
