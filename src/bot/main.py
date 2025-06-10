import asyncio

from loguru import logger
import uvloop

from bot.core.config import bot_config
from bot.core.consumer import start_redis_consumer
from bot.core.loader import bot, dp
from bot.handlers import register_handlers_routers
from bot.keyboards.commands import default_commands
from bot.middlewares import register_middlewares
from common.environment.config import env_config
from common.logging.setup import setup_module_logging
from common.sentry.setup import setup_sentry


__all__ = ()


async def on_startup() -> None:
    register_middlewares(dp)
    register_handlers_routers(dp)

    await bot.set_my_commands(default_commands)


async def on_shutdown() -> None:
    await bot.delete_webhook()
    await bot.session.close()


async def main() -> None:
    setup_module_logging("bot")
    setup_sentry()

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    if bot_config.use_webhook:
        logger.debug("Setup webhook")
        await bot.set_webhook(
            str(bot_config.webhook_url),
            drop_pending_updates=True,
            secret_token=bot_config.webhook_token,
        )
        await dp.emit_startup()
        redis_consumer_task = asyncio.create_task(start_redis_consumer())
        await redis_consumer_task
        await dp.emit_shutdown()
    else:
        logger.debug("Start polling")
        if not env_config.debug:  # Не нужно ждать запуска бота, чтобы отправлять команды
            await bot.delete_webhook(drop_pending_updates=True)

        await dp.start_polling(bot)


if __name__ == "__main__":
    uvloop.run(main())
