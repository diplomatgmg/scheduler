from aiogram import Router
from handlers import start, test


def get_handlers_router() -> Router:
    router = Router()

    router.include_routers(
        start.router,
        test.router,
    )

    return router
