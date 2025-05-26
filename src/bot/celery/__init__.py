from bot.celery.beat_schedule import beat_schedule  # isort: skip: must be before importing celery_app
import logging

from bot.celery.app import celery_app, celery_loop
from common.logging.config import log_config


# Custom logging filter to suppress kombu.pidbox debug logs
class KombuPidboxFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:  # noqa: PLR6301
        return not (record.name == "kombu.pidbox" and record.levelname == log_config.level.debug)


logging.getLogger("kombu.pidbox").addFilter(KombuPidboxFilter())

__all__ = [
    "beat_schedule",
    "celery_app",
    "celery_loop",
]
