from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject

from bot.keyboards.inline.location import location_selection_keyboard
from bot.states.location import LocationState


if TYPE_CHECKING:
    from aiogram.fsm.context import FSMContext

    from common.database.models import UserModel


class LocationMiddleware(BaseMiddleware):
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
        current_state = await state.get_state()

        if current_state in {LocationState.waiting_for_manual_choose, LocationState.waiting_for_share}:
            return await handler(event, data)

        if not user.timezone_offset:
            await state.set_state(LocationState.waiting_for_method)
            await event.answer(
                "⚠️ Для работы с отложенными сообщениями нам нужно знать ваш часовой пояс.\n\n"
                "Вы можете поделиться геопозицией или выбрать временную зону вручную.",
                reply_markup=location_selection_keyboard(),
            )
            return None

        return await handler(event, data)
