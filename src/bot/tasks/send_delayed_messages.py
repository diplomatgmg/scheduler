from aiogram.exceptions import AiogramError
from aiogram.types import Message
from loguru import logger

from bot.celery import celery_app, celery_loop
from bot.core.loader import bot
from common.database.engine import get_db_session
from common.database.services.delayed_messages import get_delayed_messages_to_send, mark_messages_as_sent


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

    logger.debug(f"Найдено {len(messages_to_send)} отложенных сообщений для отправки.")

    sent_message_ids: list[int] = []

    for delayed_message in messages_to_send:
        chat_id = delayed_message.to_chat_id
        message = Message(bot=bot, **delayed_message.message_json)

        try:
            await bot.copy_message(
                chat_id=chat_id,
                from_chat_id=message.chat.id,
                message_id=message.message_id,
            )
            sent_message_ids.append(delayed_message.id)
        except AiogramError:
            logger.critical(f"Failed to send delayed message id={delayed_message.id}")
            continue

    async with get_db_session() as session:
        await mark_messages_as_sent(session, sent_message_ids)
