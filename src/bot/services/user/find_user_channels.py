from collections.abc import Sequence

from aiogram.types import User
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import ChannelModel
from bot.utils.user import get_username

__all__ = [
    "find_user_channels",
]


async def find_user_channels(session: AsyncSession, user: User) -> Sequence[ChannelModel]:
    logger.debug(f"Getting channels for user {get_username(user)}")

    stmt = select(ChannelModel).where(ChannelModel.user_id == user.id)
    result = await session.execute(stmt)
    return result.scalars().all()
