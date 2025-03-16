import logging
import sys
from logging import LogRecord

from loguru import logger
from sqlalchemy import log as sqlalchemy_log

from bot.core.config import settings


class InterceptHandler(logging.Handler):
    """Хендлер для перенаправления логов из logging в loguru"""

    def emit(self, record: LogRecord) -> None:
        level = logger.level(record.levelname).name
        logger.opt(depth=6, exception=record.exc_info).log(level, record.getMessage())


def init_logger() -> None:
    logger.debug("Инициализация логгера")

    logging.basicConfig(handlers=[InterceptHandler()], level=logging.DEBUG)

    # loguru уже перехватывает логи из logging
    # https://stackoverflow.com/questions/60804288/pycharm-duplicated-log-for-sqlalchemy-echo-true#new-answer
    sqlalchemy_log._add_default_handler = lambda _: None  # type: ignore

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
