import asyncio

from celery import Celery  # type: ignore[import-untyped]

from common.redis.config import redis_config


__all__ = [
    "celery_app",
    "celery_loop",
]


celery_loop = asyncio.new_event_loop()
celery_app = Celery("scheduler_tasks", broker=redis_config.dsn)

celery_app.autodiscover_tasks(["bot.tasks"])
