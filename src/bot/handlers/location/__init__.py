from aiogram import Router

from bot.handlers.location import (
    location_shared,
    offset_selected,
    process_offset_selection,
    request_location,
    share_location,
)


__all__ = ["router"]


router = Router(name="location")
router.include_routers(
    location_shared.router,
    offset_selected.router,
    process_offset_selection.router,
    request_location.router,
    share_location.router,
)
