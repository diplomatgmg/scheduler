from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from common.database.models import ChannelModel
from common.database.services.user.find_user_channels import find_user_channels
from common.redis.decorators import invalidate_cache
from common.redis.decorators.cache import build_key


__all__ = [
    "add_user_channel",
]


def key_builder(_session: AsyncSession, user_id: int, _channel_model: ChannelModel) -> str:
    return build_key(user_id)


@invalidate_cache(find_user_channels, key_builder)
async def add_user_channel(
    session: AsyncSession,
    user_id: int,
    channel_model: ChannelModel,
) -> ChannelModel:
    """Добавляет канал пользователя в БД, если его ещё нет."""
    logger.debug(f"Adding channel_id={channel_model.id} for user id={user_id}")

    stmt = select(ChannelModel).where(ChannelModel.user_id == user_id, ChannelModel.chat_id == channel_model.chat_id)
    result = await session.execute(stmt)
    existing_channel = result.scalar_one_or_none()

    if not existing_channel:
        logger.debug(f"Chat_id={channel_model.id} not found for user_id={user_id}. Adding")

        session.add(channel_model)
        await session.flush()

        return channel_model

    logger.debug(f"Channel chat_id={channel_model.chat_id} found for user_id={user_id}. Updating")

    existing_channel.title = channel_model.title
    existing_channel.username = channel_model.username

    await session.flush()

    return channel_model
