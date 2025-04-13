import logging
import sys
from logging import LogRecord
from pathlib import Path

from loguru import logger

from bot.core import settings

__all__ = [
    "init_logger",
]

LOG_DIR = Path(__name__).parent / "logs"


class InterceptHandler(logging.Handler):
    """Хендлер для перенаправления логов из logging в loguru."""

    def emit(self, record: LogRecord) -> None:  # noqa: PLR6301
        level = logger.level(record.levelname).name
        logger.opt(depth=6, exception=record.exc_info).log(level, record.getMessage())


def setup_root_logging() -> None:
    logger.info("Инициализация root логгера")

    # Перехватывает логи из logging в loguru
    logging.basicConfig(handlers=[InterceptHandler()], level=logging.DEBUG)

    logger.remove()
    logger.add(
        sys.stdout,
        level=settings.LOG.level,
        colorize=True,
    )


def setup_module_logging(module_name: str) -> None:
    """
    Инициализирует логгер под модуль.
    Создает файл логов для модуля.
    """

    def make_log_path(m: str) -> Path:
        return LOG_DIR / m / f"{m}.log"

    module_logger = logger.bind(name=module_name)

    if not settings.debug:
        module_logger.add(
            make_log_path(module_name),
            rotation="1 MB",
            retention="7 days",
            compression="zip",
            level=settings.LOG.level,
        )

    logger.info(f'Логгер для модуля "{module_name}" инициализирован')


def init_logger() -> None:
    logger.info("Инициализация логгера")
    setup_root_logging()
    setup_module_logging("bot")
