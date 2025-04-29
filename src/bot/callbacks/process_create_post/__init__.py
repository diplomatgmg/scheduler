from aiogram import Router

from bot.callbacks.process_create_post.back import back_router
from bot.callbacks.process_create_post.select_channel import create_post_router
from bot.callbacks.process_create_post.send_text import send_text_router
from bot.callbacks.process_create_post.wait_text import wait_text_router

__all__ = [
    "router",
]


router = Router(name="process_create_post")
router.include_routers(
    create_post_router,
    back_router,
    wait_text_router,
    send_text_router,
)
