from typing import Any

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from common.database.exceptions import UserDoesNotExistError
from common.database.models import UserModel
from common.database.services.user import find_user
from common.redis.decorators import invalidate_cache
from common.redis.decorators.cache import build_key


def key_builder(_: AsyncSession, user_id: int, **__: Any) -> str:
    return build_key(user_id)


@invalidate_cache(find_user, key_builder)
async def update_user(session: AsyncSession, user_id: int, **fields_to_update: object) -> UserModel:
    """Обновляет поля пользователя в БД"""
    logger.debug(f"Updating user id={user_id}")

    user = await find_user(session, user_id)

    if user is None:
        raise UserDoesNotExistError

    for field, value in fields_to_update.items():
        if hasattr(user, field) and getattr(user, field) != value:
            setattr(user, field, value)
            logger.debug(f"Set {field}={value} for user id={user_id}")
        else:
            msg = f'UserModel has no attribute "{field}"'
            raise AttributeError(msg)

    await session.flush()
    await session.refresh(user)

    return user
