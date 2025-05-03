from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject

from common.database.models import UserModel
from common.database.services.user import add_user, find_user


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

__all__ = [
    "AuthMiddleware",
]


class AuthMiddleware(BaseMiddleware):
    """Добавляет пользователя в базу, если он ещё не создан."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        if not isinstance(event, Message):
            return await handler(event, data)

        session: AsyncSession = data["session"]
        user = event.from_user

        if user is None:
            return await handler(event, data)

        if await find_user(session, user.id):
            return await handler(event, data)

        user_model = UserModel(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
        )
        await add_user(session=session, user_model=user_model)

        return await handler(event, data)
