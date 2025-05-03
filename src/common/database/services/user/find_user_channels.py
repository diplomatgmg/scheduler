from collections.abc import Sequence

from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from common.database.models import ChannelModel


__all__ = [
    "find_user_channels",
]


async def find_user_channels(session: AsyncSession, user_id: int) -> Sequence[ChannelModel]:
    """Возвращает каналы пользователя из БД."""
    logger.debug(f"Getting channels for user id={user_id}")

    stmt = select(ChannelModel).where(ChannelModel.user_id == user_id)
    result = await session.execute(stmt)
    return result.scalars().all()
