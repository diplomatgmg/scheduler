import logging
from logging.handlers import RotatingFileHandler

from core import config


def setup_logger():
    root_logger = logging.getLogger()
    root_logger.propagate = False

    root_logger.setLevel(config.LOG_LEVEL.value)
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    if not config.DEBUG:
        file_handler = RotatingFileHandler("app.log", maxBytes=1000000, backupCount=5)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    root_logger.debug("Логгер инициализирован")
