from loguru import logger
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from common.database.models import ChannelModel


__all__ = [
    "add_user_channel",
]


async def add_user_channel(
    session: AsyncSession,
    user_id: int,
    channel: ChannelModel,
) -> ChannelModel | None:
    """Добавляет канал пользователя в БД, если его ещё нет."""
    logger.debug(f"Adding channel id={channel.id} for user id={user_id}")

    session.add(channel)

    try:
        await session.commit()
    except IntegrityError:
        logger.warning(f"Channel id={channel.id} already exists for user id={user_id}")
        await session.rollback()
        return None

    return channel
