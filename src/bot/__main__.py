import uvloop
from loguru import logger

from bot.callbacks import register_callbacks_routers
from bot.core import settings
from bot.core.loader import bot, dp
from bot.core.logger import init_logger
from bot.db.engine import init_db
from bot.handlers import register_handlers_routers
from bot.middlewares import register_middlewares


def on_startup() -> None:
    register_middlewares(dp)
    register_handlers_routers(dp)
    register_callbacks_routers(dp)


async def main() -> None:
    init_logger()
    logger.info(f"Environment mode: {settings.ENV.mode}")
    await init_db()

    dp.startup.register(on_startup)

    await dp.start_polling(bot)


if __name__ == "__main__":
    uvloop.run(main())
