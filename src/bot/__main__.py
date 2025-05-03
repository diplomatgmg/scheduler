from loguru import logger
import uvloop

from bot.core.loader import bot, dp
from bot.handlers import register_handlers_routers
from bot.keyboards import default_commands
from bot.middlewares import register_middlewares
from common.environment.config import env_config
from common.logging.config import log_config
from common.logging.logger import setup_logging, setup_module_logging
from common.sentry.setup import setup_sentry


__all__ = ()


async def on_startup() -> None:
    if not env_config.debug:  # Не нужно ждать запуска бота, чтобы отправлять команды
        await bot.delete_webhook(drop_pending_updates=True)

    register_middlewares(dp)
    register_handlers_routers(dp)

    await bot.set_my_commands(default_commands)


async def on_shutdown() -> None:
    await bot.delete_webhook()
    await bot.session.close()


async def main() -> None:
    logger.info(f"Env mode: {env_config.mode}, log level: {log_config.level}")

    setup_logging()
    setup_module_logging("bot")
    setup_sentry()

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await dp.start_polling(bot)


if __name__ == "__main__":
    uvloop.run(main())
