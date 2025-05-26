from loguru import logger

from bot.celery import celery_app, celery_loop
from common.database.engine import get_db_session
from common.database.services.messages import get_delayed_messages_to_send


__all__ = ()


@celery_app.task(name="send_delayed_messages")  # type: ignore[misc]
def send_delayed_messages() -> None:
    celery_loop.run_until_complete(send_messages_from_db())


async def send_messages_from_db() -> None:
    """
    Асинхронная функция, которая извлекает сообщения из БД и отправляет их.
    """
    async with get_db_session() as session:
        messages_to_send = await get_delayed_messages_to_send(session)

    if not messages_to_send:
        logger.debug("Нет отложенных сообщений для отправки.")
        return

    logger.info(f"Найдено {len(messages_to_send)} отложенных сообщений для отправки.")

    for message in messages_to_send:
        logger.info(message)
