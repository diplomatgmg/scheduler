from aiogram.types import User
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import UserModel


async def add_user(session: AsyncSession, user: User) -> None:
    logger.debug(f"Создаем пользователя id={user.id}")

    user_model = UserModel(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
    )

    session.add(user_model)
    await session.commit()
