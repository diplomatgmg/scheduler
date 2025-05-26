from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from common.database.models import DelayedMessageModel


__all__ = [
    "save_delayed_message",
]


async def save_delayed_message(session: AsyncSession, message_model: DelayedMessageModel) -> None:
    """Добавляет сообщение для отложки в БД."""
    logger.debug(f"Adding delayed message id={message_model.id}")

    session.add(message_model)
    await session.flush()
    await session.refresh(message_model)
