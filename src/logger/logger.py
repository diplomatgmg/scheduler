import logging
import sys

from loguru import logger

from bot.core.config import settings


class InterceptHandler(logging.Handler):
    """Хендлер для перенаправления логов из logging в loguru"""

    def emit(self, record):
        level = logger.level(record.levelname).name
        logger.opt(depth=6, exception=record.exc_info).log(level, record.getMessage())


logging.basicConfig(handlers=[InterceptHandler()], level=logging.DEBUG)


logger.remove()
logger.add(
    sys.stdout,
    level=settings.LOG_LEVEL.value,
)

bot_logger = logger.bind(name="bot")
bot_logger.add(
    "logs/bot/bot.log",
    rotation="1 MB",
    retention="7 days",
    compression="zip",
    level=settings.LOG_LEVEL.value,
)
