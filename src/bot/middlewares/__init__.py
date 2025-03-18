from __future__ import annotations

from typing import TYPE_CHECKING

from loguru import logger

from bot.middlewares.database import DatabaseMiddleware

if TYPE_CHECKING:
    from aiogram import Dispatcher


def register_middlewares(dp: Dispatcher) -> None:
    logger.debug("Регистрация middlewares")
    dp.update.outer_middleware(DatabaseMiddleware())
