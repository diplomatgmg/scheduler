from aiogram import Router
from src.bot.handlers import test
from src.bot.handlers import start


def get_handlers_router() -> Router:
    router = Router()

    router.include_routers(
        start.router,
        test.router,
    )

    return router
