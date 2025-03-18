from __future__ import annotations

from typing import TYPE_CHECKING

from loguru import logger

from bot.callbacks import menu

if TYPE_CHECKING:
    from aiogram import Dispatcher


def register_callbacks_routers(dp: Dispatcher) -> None:
    logger.debug("Регистрация callbacks routers")

    dp.include_routers(
        menu.router,
    )
