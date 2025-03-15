from aiogram import Router
from bot.handlers import test
from bot.handlers import start


def get_handlers_router() -> Router:
    router = Router()

    router.include_routers(
        start.router,
        test.router,
    )

    return router
