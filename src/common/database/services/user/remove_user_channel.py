from loguru import logger
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from common.database.models import ChannelModel


__all__ = [
    "remove_user_channel",
]


async def remove_user_channel(
    session: AsyncSession,
    user_id: int,
    chat_id: int,
) -> bool:
    """Удаляет канал пользователя из базы данных."""
    logger.debug(f"Removing channel id={chat_id} for user id={user_id}")

    stmt = delete(ChannelModel).where(ChannelModel.user_id == user_id, ChannelModel.chat_id == chat_id)

    result = await session.execute(stmt)
    await session.flush()

    if result.rowcount == 0:
        logger.warning(f"No channel found for user id={user_id} with chat_id={chat_id}")
        return False

    return True
