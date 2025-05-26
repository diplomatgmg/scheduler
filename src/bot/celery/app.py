import asyncio

from celery import Celery  # type: ignore[import-untyped]

from bot.celery.config import celery_config


__all__ = [
    "celery_app",
    "celery_loop",
]


celery_loop = asyncio.new_event_loop()
celery_app = Celery("scheduler_tasks", broker=str(celery_config.connection.dsn))

celery_app.autodiscover_tasks(["bot.tasks"])
