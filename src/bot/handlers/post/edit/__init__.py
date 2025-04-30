from aiogram import Router

from bot.handlers.post.edit import edit_post

__all__ = [
    "router",
]


router = Router(name="edit")
router.include_routers(
    edit_post.router,
)
