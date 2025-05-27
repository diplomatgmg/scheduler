from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from common.database.models import DelayedMessageModel


__all__ = [
    "save_delayed_message",
]


async def save_delayed_message(session: AsyncSession, message_model: DelayedMessageModel) -> None:
    """Добавляет сообщение для отложки в БД."""
    session.add(message_model)
    await session.flush()

    logger.debug(f"Adding delayed message update_id={message_model.id}")
