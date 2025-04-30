from aiogram import Router

from bot.handlers.post import create, edit

__all__ = ["router"]


router = Router(name="post")
router.include_routers(
    create.router,
    edit.router,
)
