from aiogram import Router

from bot.handlers.post.create import (
    add_buttons,
    cancel_add_buttons,
    remove_buttons,
    select_channel,
    send_buttons,
    send_text,
    wait_text,
)


__all__ = [
    "router",
]


router = Router(name="create")
router.include_routers(
    select_channel.router,
    send_text.router,
    wait_text.router,
    add_buttons.router,
    cancel_add_buttons.router,
    send_buttons.router,
    remove_buttons.router,
)
