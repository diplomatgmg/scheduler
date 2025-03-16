import uvloop

from bot.callbacks import get_callbacks_router
from bot.core.config import settings
from bot.core.loader import bot, dp
from bot.db.engine import init_db
from bot.handlers import get_handlers_router
from bot.middlewares import register_middlewares
from logger import bot_logger, init_logger


async def on_startup() -> None:
    init_logger()
    await init_db()

    register_middlewares(dp)
    dp.include_router(get_handlers_router())
    dp.include_router(get_callbacks_router())


async def main() -> None:
    bot_logger.debug(f"Уровень логирования: {settings.LOG_LEVEL.value}")

    dp.startup.register(on_startup)

    await dp.start_polling(bot)


if __name__ == "__main__":
    uvloop.run(main())
