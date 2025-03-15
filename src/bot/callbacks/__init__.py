from aiogram import Router
from bot.callbacks import menu


def get_callbacks_router() -> Router:
    router = Router()

    router.include_routers(
        menu.router,
    )

    return router
