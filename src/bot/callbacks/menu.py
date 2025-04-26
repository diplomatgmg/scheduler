from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from bot.callbacks.utils import make_linked
from bot.keyboards.inline.menu import select_channel_keyboard
from bot.schemas.menu import ChannelSelectCallback, MenuActionEnum, MenuCallback
from bot.services.user import find_user_channels
from bot.states.post import PostState
from bot.utils.messages import safe_reply
from bot.utils.user import get_username

router = Router(name="menu")


# FIXME Хотелось бы изменить структуру для каждого MenuAction. menu > (create, edit, settings)


# mypy корректно видит тип, ide - нет
# noinspection PyTypeChecker
@router.callback_query(MenuCallback.filter(F.action == MenuActionEnum.CREATE))
async def handle_create_callback(query: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    logger.debug(f"[CREATE] callback from {get_username(query)}")

    channels = await find_user_channels(session, query.from_user)
    if not channels:
        await safe_reply(query, "Бот не является администратором ни одного канала.")
        return

    await state.clear()
    await state.set_state(PostState.waiting_for_channel)

    if isinstance(query.message, Message):
        await query.message.edit_text(
            text="Выберите канал для публикации:", reply_markup=select_channel_keyboard(channels)
        )
    else:
        pass
        # FIXME Не до конца понимаю типизацию. По идеи гарантированно должен быть message
        #  (Вроде если сообщение удаляется, то используется другой тип,
        #  но если бот (или пользователь не удаляет сообщение?)


@router.callback_query(ChannelSelectCallback.filter(), PostState.waiting_for_channel)
async def handle_channel_selected(
    query: CallbackQuery, callback_data: ChannelSelectCallback, state: FSMContext
) -> None:
    selected_channel_title = callback_data.channel_title
    selected_channel_username = callback_data.channel_username

    logger.debug(f"[CHANNEL_SELECT] Channel '{selected_channel_title}' selected by {get_username(query)}")

    await query.answer()

    await state.update_data(selected_channel_title=selected_channel_title)
    await state.set_state(PostState.waiting_for_text)

    if isinstance(query.message, Message):
        linked = make_linked(selected_channel_title, selected_channel_username)

        message_text = f"Вы выбрали канал: {linked}\n\nТеперь отправьте мне текст для публикации."

        await query.message.edit_text(
            message_text,
            parse_mode="HTML",
        )
    else:
        # FIXME см. handle_create_callback
        pass


@router.message(PostState.waiting_for_text, F.text)
async def handle_post_text(message: Message, state: FSMContext) -> None:
    """Обрабатывает полученный текст для публикации."""
    logger.debug(f"[POST_TEXT] Received text from {get_username(message)}")

    user_data = await state.get_data()

    # FIXME. Немного не понял.
    #  До этого использовал callback_data, а тут опбращение по ключу.
    selected_channel_title = user_data.get("selected_channel_title")

    # FIXME Понять в каких ситуациях это происходит
    if not selected_channel_title:
        logger.error(f"No selected channel found in state for user {get_username(message)}")
        await message.reply("Произошла ошибка. Пожалуйста, попробуйте начать создание поста сначала.")
        await state.clear()
        return

    post_text = message.text

    await message.answer(
        f"Получен текст для публикации в канал <{selected_channel_title}':\n\n"
        f"{post_text}\n\n"
        "Функция публикации пока не реализована. Состояние FSM сброшено."
    )

    # FIXME Пока не до конца понял, в каких ситуациях необходимо сбрасывать состояния
    await state.clear()


# noinspection PyTypeChecker
@router.callback_query(MenuCallback.filter(F.action == MenuActionEnum.SETTINGS))
async def handle_settings_callback(
    query: CallbackQuery,
    state: FSMContext,
) -> None:
    logger.debug(f"[SETTINGS] callback from {get_username(query)}")
    await query.answer("Настройки открыты")
    await state.clear()


# noinspection PyTypeChecker
@router.callback_query(MenuCallback.filter(F.action == MenuActionEnum.EDIT))
async def handle_edit_callback(
    query: CallbackQuery,
    state: FSMContext,
) -> None:
    logger.debug(f"[EDIT] callback from {get_username(query)}")
    await query.answer("Режим редактирования")
    await state.clear()
