from aiogram.types import Chat, User
from loguru import logger
from sqlalchemy import delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from bot.utils.user import get_username
from common.database.models import ChannelModel

__all__ = [
    "remove_user_channel",
]


async def remove_user_channel(
    session: AsyncSession,
    user: User,
    chat: Chat,
) -> bool:
    """
    Удаляет канал пользователя из базы данных.
    """
    logger.debug(f"Removing channel {get_username(chat)} for user {get_username(user)}")

    stmt = delete(ChannelModel).where(ChannelModel.user_id == user.id, ChannelModel.chat_id == chat.id)

    try:
        result = await session.execute(stmt)
        await session.commit()

        if result.rowcount == 0:
            logger.warning(f"No channel found for user {user.id} with chat_id {chat.id}")
            return False

        logger.info(f"Channel {chat.id} successfully removed for user {user.id}")

    except SQLAlchemyError as e:
        logger.error(f"Failed to remove channel {chat.id} for user {user.id}: {e}")
        await session.rollback()
        return False

    return True
