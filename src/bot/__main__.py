import uvloop

from bot.callbacks import get_callbacks_router
from logger import bot_logger
from bot.core.config import settings
from bot.core.loader import bot, dp
from bot.handlers import get_handlers_router


async def main() -> None:
    bot_logger.success(f"Режим разработки - {settings.ENVIRONMENT.value}")
    bot_logger.success(f"Уровень логирования: {settings.LOG_LEVEL.value}")

    dp.include_router(get_handlers_router())
    dp.include_router(get_callbacks_router())

    await dp.start_polling(bot)


if __name__ == "__main__":
    uvloop.run(main())
