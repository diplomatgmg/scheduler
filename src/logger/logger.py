import logging
import sys
from logging import LogRecord
from pathlib import Path
from typing import Callable

from loguru import logger

from bot.core.config import settings

LOG_DIR = Path(__name__).parent / "logs"


class InterceptHandler(logging.Handler):
    """Хендлер для перенаправления логов из logging в loguru."""

    def emit(self, record: LogRecord) -> None:
        level = logger.level(record.levelname).name
        logger.opt(depth=6, exception=record.exc_info).log(level, record.getMessage())


def setup_root_logging() -> None:
    # Перехватывает логи из logging в loguru
    logging.basicConfig(handlers=[InterceptHandler()], level=logging.DEBUG)

    logger.remove()
    logger.add(
        sys.stdout,
        level=settings.LOG_LEVEL.value,
        colorize=True,
    )


def setup_module_logging(module_name: str) -> None:
    make_log_path: Callable[[str], Path] = lambda m: LOG_DIR / m / f"{m}.log"

    module_logger = logger.bind(name=module_name)
    module_logger.add(
        make_log_path(module_name),
        rotation="1 MB",
        retention="7 days",
        compression="zip",
        level=settings.LOG_LEVEL.value,
    )

    logger.debug(f'Логгер для модуля "{module_name}" инициализирован')


def init_logger() -> None:
    logger.debug("Инициализация логгера")
    setup_root_logging()
    setup_module_logging("bot")
