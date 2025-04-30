from aiogram import Router

from bot.handlers.settings import settings

__all__ = [
    "router",
]


router = Router(name="process_settings")
router.include_routers(
    settings.router,
)
