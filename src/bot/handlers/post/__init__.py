from aiogram import Router

from bot.handlers.post import create, edit, schedule


__all__ = ["router"]


router = Router(name="post")
router.include_routers(
    create.router,
    edit.router,
    schedule.router,
)
