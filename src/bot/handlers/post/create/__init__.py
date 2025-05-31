from aiogram import Router

from bot.handlers.post.create import (
    channel_selection,
    manage_post_buttons,
    post_creation,
    process_buttons,
    process_post,
    request_buttons,
    schedule_post,
)


__all__ = [
    "channel_selection",
    "manage_post_buttons",
    "post_creation",
    "process_buttons",
    "process_post",
    "request_buttons",
    "schedule_post",
]


router = Router(name="create")
router.include_routers(
    post_creation.router,
    channel_selection.router,
    process_post.router,
    request_buttons.router,
    process_buttons.router,
    manage_post_buttons.router,
    schedule_post.router,
)
