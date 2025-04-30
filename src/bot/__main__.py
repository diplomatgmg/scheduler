import uvloop
from loguru import logger

from bot.core import settings
from bot.core.loader import bot, dp
from bot.core.logger import init_logger
from bot.core.settings.sentry import init_sentry
from bot.handlers import register_handlers_routers
from bot.keyboards import default_commands
from bot.middlewares import register_middlewares


async def on_startup() -> None:
    if not settings.debug:  # Не нужно ждать запуска бота, чтобы отправлять команды
        await bot.delete_webhook(drop_pending_updates=True)

    register_middlewares(dp)
    register_handlers_routers(dp)

    await bot.set_my_commands(default_commands)


async def on_shutdown() -> None:
    await bot.delete_webhook()
    await bot.session.close()


async def main() -> None:
    logger.info(f"Env mode: {settings.ENV.mode}, log level: {settings.LOG.level}")

    init_logger()
    init_sentry()

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await dp.start_polling(bot)


if __name__ == "__main__":
    uvloop.run(main())
