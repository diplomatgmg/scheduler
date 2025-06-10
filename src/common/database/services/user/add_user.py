from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from common.database.models import UserModel
from common.database.services.user.find_user import find_user
from common.redis.decorators import invalidate_cache
from common.redis.decorators.cache import build_key


__all__ = [
    "add_user",
]


def key_builder(_: AsyncSession, user_model: UserModel) -> str:
    return build_key(user_model.id)


@invalidate_cache(find_user, key_builder)
async def add_user(session: AsyncSession, user_model: UserModel) -> UserModel:
    """Добавляет пользователя в БД."""
    logger.debug(f"Adding user id={user_model.id}")

    session.add(user_model)
    await session.flush()
    await session.refresh(user_model)

    return user_model
