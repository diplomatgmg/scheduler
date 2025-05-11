from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from common.database.models import UserModel
from common.redis.decorators import cache


__all__ = [
    "find_user",
]


@cache()
async def find_user(session: AsyncSession, user_id: int) -> UserModel | None:
    """Возвращает пользователя из БД."""
    logger.debug(f"Getting user id={user_id}")

    query = select(UserModel).where(UserModel.id == user_id)
    result = await session.execute(query)
    return result.scalar_one_or_none()
