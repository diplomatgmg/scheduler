from __future__ import annotations

from typing import TYPE_CHECKING

from loguru import logger

from bot.handlers import start, test

if TYPE_CHECKING:
    from aiogram import Dispatcher


def register_handlers_routers(dp: Dispatcher) -> None:
    logger.debug("Регистрация handlers routers")

    dp.include_routers(
        start.router,
        test.router,
    )
