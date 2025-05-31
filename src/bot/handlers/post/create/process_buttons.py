from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, Message
from loguru import logger

from bot.core.loader import bot
from bot.keyboards.inline.post import post_additional_configuration_keyboard, post_cancel_buttons
from bot.schemas import PostContext
from bot.states.post import PostCreateState
from bot.utils.user import get_username
from common.schemas.url import HttpsUrl


__all__ = ["router"]


router = Router(name="process_buttons")


def parse_buttons(buttons_str: str) -> list[list[InlineKeyboardButton]]:
    url_buttons: list[list[InlineKeyboardButton]] = []

    row_buttons_str = buttons_str.strip().split("\n")

    for row in row_buttons_str:
        buttons_in_row: list[InlineKeyboardButton] = []
        buttons_in_row_str = row.split("|")

        for button_str in buttons_in_row_str:
            try:
                text, url = map(str.strip, button_str.split("-", maxsplit=1))
                button = InlineKeyboardButton(text=text, url=str(HttpsUrl(url)))
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
    await state.set_state(PostCreateState.process_buttons)


@router.message(PostCreateState.process_buttons)
async def handle_process_buttons(message: Message, state: FSMContext) -> None:
    """Обрабатывает кнопки, которые необходимо прикрепить к посту."""
    logger.debug(f"Send buttons callback from {get_username(message)}")

    post_context = PostContext(**await state.get_data())

    if message.text is None or post_context.preview_message is None:
        await try_again(message, state)
        return

    try:
        buttons = parse_buttons(message.text)
    except ValueError:
        await try_again(message, state)
        return

    post_context.preview_message.buttons = buttons

    await bot.copy_message(
        chat_id=message.chat.id,
        from_chat_id=post_context.preview_message.message.chat.id,
        message_id=post_context.preview_message.message.message_id,
        reply_markup=post_additional_configuration_keyboard(buttons),
    )

    await state.set_state(PostCreateState.process_post)
