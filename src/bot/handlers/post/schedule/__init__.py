from aiogram import Router

from bot.handlers.post.schedule import (
    publish_now,
    schedule,
    set_delete_timer,
)


__all__ = ["router"]


router = Router(name="schedule")
router.include_routers(
    publish_now.router,
    schedule.router,
    set_delete_timer.router,
)
