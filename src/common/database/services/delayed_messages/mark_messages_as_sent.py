from collections.abc import Sequence

from loguru import logger
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from common.database.models import DelayedMessageModel


__all__ = [
    "mark_messages_as_sent",
]


async def mark_messages_as_sent(session: AsyncSession, message_ids: Sequence[int]) -> None:
    """Помечает отложенное сообщение как отправленное."""
    logger.debug(f"Marking delayed messages as sent ids={message_ids}")

    query = update(DelayedMessageModel).where(DelayedMessageModel.id.in_(message_ids)).values(is_sent=True)
    await session.execute(query)
    await session.flush()
