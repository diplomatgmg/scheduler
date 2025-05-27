from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from loguru import logger

from bot.keyboards.inline.post import post_cancel_buttons
from bot.schemas.post import UrlButton
from bot.states import PostState
from bot.utils.user import get_username
from common.schemas.url import HttpsUrl


__all__ = [
    "router",
]


router = Router(name="wait_buttons")


def parse_buttons(buttons_str: str) -> list[list[UrlButton]]:
    url_buttons: list[list[UrlButton]] = []

    row_buttons_str = buttons_str.strip().split("\n")

    for row in row_buttons_str:
        buttons_in_row: list[UrlButton] = []
        buttons_in_row_str = row.split("|")

        for button_str in buttons_in_row_str:
            try:
                text, url = map(str.strip, button_str.split("-", maxsplit=1))
                button = UrlButton(text=text, url=HttpsUrl(url))
                buttons_in_row.append(button)
            except ValueError as e:
                msg = f"Ошибка при разборе кнопки '{button_str}': {e!s}"
                raise ValueError(msg) from e

        url_buttons.append(buttons_in_row)

    return url_buttons


async def try_again(message: Message, state: FSMContext) -> None:
    await message.answer(
        "Прислан некорректный формат кнопок. Попробуйте еще раз",
        reply_markup=post_cancel_buttons(),
    )
    await state.set_state(PostState.waiting_for_buttons)


@router.message(PostState.waiting_for_buttons)
async def handle_send_buttons(message: Message, state: FSMContext) -> None:
    """Обработчик для получения поста, который необходимо создать на канале"""
    logger.debug(f"Send buttons callback from {get_username(message)}")
    if message.text is None:
        await try_again(message, state)
        return

    try:
        parse_buttons(message.text)
    except ValueError:
        await try_again(message, state)
        return

    await message.answer("Еще не реализовано")
