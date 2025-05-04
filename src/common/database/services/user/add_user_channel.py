from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from common.database.models import ChannelModel


__all__ = [
    "add_user_channel",
]


async def add_user_channel(
    session: AsyncSession,
    user_id: int,
    channel_model: ChannelModel,
) -> ChannelModel | None:
    """Добавляет канал пользователя в БД, если его ещё нет."""
    logger.debug(f"Adding channel_id={channel_model.id} for user id={user_id}")

    stmt = select(ChannelModel).where(ChannelModel.user_id == user_id, ChannelModel.chat_id == channel_model.chat_id)
    result = await session.execute(stmt)
    existing_channel = result.scalar_one_or_none()

    if existing_channel:
        logger.debug(f"Channel chat_id={channel_model.chat_id} found for user_id={user_id}. Updating")
        existing_channel.title = channel_model.title
        existing_channel.username = channel_model.username
        await session.commit()

        return existing_channel

    logger.debug(f"Chat_id={channel_model.id} not found for user_id={user_id}. Creating")

    session.add(channel_model)
    await session.commit()
    await session.refresh(channel_model)

    return channel_model
