from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from common.database.models import UserModel
from common.redis.decorators import cache
from common.redis.decorators.cache import build_key


__all__ = [
    "find_user",
]


def _key_builder(_: AsyncSession, user_id: int) -> str:
    return build_key(user_id)


@cache(key_builder=_key_builder)
async def find_user(session: AsyncSession, user_id: int) -> UserModel | None:
    """Возвращает пользователя из БД."""
    logger.debug(f"Getting user id={user_id}")

    query = select(UserModel).where(UserModel.id == user_id)
    result = await session.execute(query)
    return result.scalar_one_or_none()
