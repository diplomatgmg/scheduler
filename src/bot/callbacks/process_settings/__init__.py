from aiogram import Router

from bot.callbacks.process_settings.settings import settings_router

__all__ = [
    "router",
]


router = Router(name="process_settings")
router.include_routers(
    settings_router,
)
