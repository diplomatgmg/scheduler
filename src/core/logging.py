from pathlib import Path

import logging
from core.config import config


def setup_logging():
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    log_format = "%(asctime)s %(levelname)s %(name)s: %(message)s"

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if config.DEBUG else logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(logging.Formatter(log_format))

    debug_handler = logging.FileHandler(log_dir / "debug.log")
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(logging.Formatter(log_format))

    info_handler = logging.FileHandler(log_dir / "info.log")
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(logging.Formatter(log_format))

    warning_handler = logging.FileHandler(log_dir / "warning.log")
    warning_handler.setLevel(logging.WARNING)
    warning_handler.setFormatter(logging.Formatter(log_format))

    error_handler = logging.FileHandler(log_dir / "error.log")
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(logging.Formatter(log_format))

    critical_handler = logging.FileHandler(log_dir / "critical.log")
    critical_handler.setLevel(logging.CRITICAL)
    critical_handler.setFormatter(logging.Formatter(log_format))

    logger.addHandler(debug_handler)
    logger.addHandler(info_handler)
    logger.addHandler(warning_handler)
    logger.addHandler(error_handler)
    logger.addHandler(critical_handler)
    logger.addHandler(console_handler)
