from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject

from bot.services.user import add_user, find_user

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

__all__ = [
    "AuthMiddleware",
]


class AuthMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        message: Message,  # type: ignore[override]
        data: dict[str, Any],
    ):
        session: AsyncSession = data["session"]
        user = message.from_user

        if user is None:
            return await handler(message, data)

        if await find_user(session, user.id):
            return await handler(message, data)

        await add_user(session=session, user=user)

        return await handler(message, data)
