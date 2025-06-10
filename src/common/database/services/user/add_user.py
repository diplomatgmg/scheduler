from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from common.database.models import UserModel


__all__ = [
    "add_user",
]


async def add_user(session: AsyncSession, user_model: UserModel) -> UserModel:
    """Добавляет пользователя в БД."""
    logger.debug(f"Adding user id={user_model.id}")

    session.add(user_model)
    await session.flush()
    await session.refresh(user_model)

    return user_model
