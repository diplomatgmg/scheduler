from aiogram import Dispatcher
from loguru import logger

from bot.callbacks import process_create_post, process_edit_post, process_settings

__all__ = [
    "process_create_post",
    "register_callbacks_routers",
]


def register_callbacks_routers(dp: Dispatcher) -> None:
    logger.debug("Registering callback routers")

    dp.include_routers(
        process_create_post.router,
        process_edit_post.router,
        process_settings.router,
    )
