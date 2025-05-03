from aiogram import Router

from bot.handlers.post.create import select_channel, send_text, wait_text


__all__ = [
    "router",
]


router = Router(name="create")
router.include_routers(select_channel.router, send_text.router, wait_text.router)
