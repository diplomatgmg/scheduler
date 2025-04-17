from aiogram.types import Chat, User
from loguru import logger
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import ChannelModel
from bot.utils.user import get_username

__all__ = [
    "add_user_channel",
]


async def add_user_channel(
    session: AsyncSession,
    user: User,
    chat: Chat,
) -> ChannelModel | None:
    """Добавляет канал пользователя в БД, если его ещё нет."""
    logger.debug(f"Adding channel {chat.title} for user {get_username(user)}")

    if not chat.title:
        logger.warning(f"Cannot get title for chat {get_username(chat)}")

    new_channel = ChannelModel(
        user_id=user.id,
        chat_id=chat.id,
        title=chat.title or "Без названия",
        username=chat.username,
    )

    session.add(new_channel)

    try:
        await session.commit()
    except IntegrityError:
        logger.warning(f"Channel {chat.id} already exists for user {user.id}")
        await session.rollback()
        return None

    return new_channel
