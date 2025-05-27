from collections.abc import Sequence

from loguru import logger
from sqlalchemy import not_, select
from sqlalchemy.ext.asyncio import AsyncSession

from common.database.models import DelayedMessageModel


__all__ = [
    "get_delayed_messages_to_send",
]


async def get_delayed_messages_to_send(session: AsyncSession) -> Sequence[DelayedMessageModel]:
    """Возвращает пользователя из БД."""
    logger.debug("Getting delayed messages to send")

    query = select(DelayedMessageModel).where(not_(DelayedMessageModel.is_sent))
    result = await session.execute(query)
    return result.scalars().all()
