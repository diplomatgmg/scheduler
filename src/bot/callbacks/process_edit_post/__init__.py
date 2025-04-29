from aiogram import Router

from bot.callbacks.process_edit_post.edit_post import edit_router

__all__ = [
    "router",
]


router = Router(name="process_edit_post")
router.include_routers(
    edit_router,
)
