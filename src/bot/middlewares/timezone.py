from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject

from bot.keyboards.inline.location import location_selection_keyboard
from bot.states.location import TimezoneSetupState


if TYPE_CHECKING:
    from aiogram.fsm.context import FSMContext

    from common.database.models import UserModel


class TimezoneMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        if not isinstance(event, Message):
            return await handler(event, data)

        user: UserModel = data["user"]
        state: FSMContext = data["state"]

        if await state.get_state() == TimezoneSetupState.waiting_for_timezone:
            return await handler(event, data)

        if not user.timezone_offset:
            await state.set_state(TimezoneSetupState.waiting_for_timezone)
            await request_timezone(event)
            return None

        return await handler(event, data)


async def request_timezone(message: Message) -> None:
    """Отправляет запрос на установку временной зоны"""

    await message.answer(
        "⚠️ Для работы с отложенными сообщениями нам нужно знать ваш часовой пояс.\n\n"
        "Вы можете поделиться геопозицией или выбрать временную зону вручную.",
        reply_markup=location_selection_keyboard(),
    )
