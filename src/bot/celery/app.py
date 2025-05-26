import asyncio
from typing import Any

from celery import Celery  # type: ignore[import-untyped]
from celery.signals import setup_logging as celery_logging  # type: ignore[import-untyped]

from bot.celery.config import celery_config
from common.logging.setup import setup_logging


@celery_logging.connect  # type: ignore[misc]
def setup_celery_logging(**_: Any) -> None:
    setup_logging("celery")


__all__ = [
    "celery_app",
    "celery_loop",
]


celery_loop = asyncio.new_event_loop()
celery_app = Celery("scheduler_tasks", broker=str(celery_config.connection.dsn))

celery_app.autodiscover_tasks(["bot.tasks"])
