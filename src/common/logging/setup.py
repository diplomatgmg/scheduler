import logging
from logging import LogRecord
from pathlib import Path
import sys

from loguru import logger

from common.environment.config import env_config
from common.logging.config import log_config


__all__ = [
    "setup_logging",
]


LOG_DIR = Path(__name__).parent / "logs"
_LOGGING_INITIALIZED: set[str] = set()


class InterceptHandler(logging.Handler):
    """Хендлер для перенаправления логов из logging в loguru."""

    def emit(self, record: LogRecord) -> None:  # noqa: PLR6301
        level = logger.level(record.levelname).name
        logger.opt(depth=6, exception=record.exc_info).log(level, record.getMessage())


def setup_logging(module_name: str) -> None:
    """Инициализирует logger для модуля"""

    if module_name in _LOGGING_INITIALIZED:
        return

    logger.trace(f"Env mode: {env_config.mode}, log level: {log_config.level}")
    logger.trace(f'Initializing logger for module "{module_name}"')

    # Перехватывает логи из logging в loguru
    logging.basicConfig(handlers=[InterceptHandler()], level=logging.NOTSET)

    logger.remove()
    logger.add(
        sys.stdout,
        level=log_config.level,
        colorize=True,
    )

    def make_log_path(m: str) -> Path:
        return LOG_DIR / m / f"{m}.log"

    module_logger = logger.bind(name=module_name)

    if not env_config.debug:
        module_logger.add(
            make_log_path(module_name),
            rotation="1 MB",
            retention="7 days",
            compression="zip",
            level=log_config.level,
        )

    _LOGGING_INITIALIZED.add(module_name)
