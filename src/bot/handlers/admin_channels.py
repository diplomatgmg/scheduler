from aiogram import Router
from aiogram.filters import ADMINISTRATOR, PROMOTED_TRANSITION, ChatMemberUpdatedFilter
from aiogram.types import ChatMemberAdministrator, ChatMemberUpdated
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from bot.core.loader import bot
from bot.utils.messages import make_linked
from bot.utils.user import get_username
from common.database.models import ChannelModel
from common.database.services.user import add_user_channel, remove_user_channel


__all__ = ()


router = Router(name="admin_channels")


def _get_linked_channel(event: ChatMemberUpdated) -> str:
    chat_title = event.chat.title or "Неизвестно"
    chat_username = get_username(event)
    return make_linked(chat_title, chat_username)


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=PROMOTED_TRANSITION))
async def on_bot_promoted(event: ChatMemberUpdated, session: AsyncSession) -> None:
    """Обрабатывает права бота когда он становится администратором канала"""
    logger.debug(f"Bot was promoted to administrator by user_id={event.from_user.id} in channel_id={event.chat.id}")

    linked_channel = _get_linked_channel(event)

    await bot.send_message(
        event.from_user.id,
        f"✅  Вы добавили меня в администраторы канала {linked_channel}",
        parse_mode="HTML",
    )

    await on_bot_permissions_changed(event, session)


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=~PROMOTED_TRANSITION))
async def on_bot_demoted(event: ChatMemberUpdated, session: AsyncSession) -> None:
    logger.debug(f"Bot was removed from administrators by user_id={event.from_user.id} in channel_id={event.chat.id}")

    linked_channel = _get_linked_channel(event)

    # TelegramAPI может удалить бота раньше, чем тот успеет отправить сообщение
    try:
        await bot.send_message(
            event.from_user.id,
            f"ℹ️  Я больше не администратор в канале {linked_channel}\n\n"
            f"⚠️  <b>Теперь я не смогу управлять постами в канале</b>",
            parse_mode="HTML",
        )
    finally:
        await remove_user_channel(session, event.from_user.id, event.chat.id)


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=ADMINISTRATOR))
async def on_bot_permissions_changed(event: ChatMemberUpdated, session: AsyncSession) -> None:
    logger.debug(f"Bot permissions were updated by user_id={event.from_user.id} in channel_id={event.chat.id}")

    linked_channel = _get_linked_channel(event)

    if not isinstance(event.new_chat_member, ChatMemberAdministrator):
        logger.warning(f"Expected ChatMemberAdministrator, got {type(event.new_chat_member)}")
        return

    permissions_list = (
        (event.new_chat_member.can_post_messages, "Могу отправлять сообщения в канал"),
        (event.new_chat_member.can_delete_messages, "Могу удалять сообщения в канале"),
    )

    message_permissions = ""
    all_granted = True

    for has_permission, description in permissions_list:
        emoji = "✅" if has_permission else "❌"
        message_permissions += f"    {emoji} {description}\n"
        if not has_permission:
            all_granted = False

    if not all_granted:
        await bot.send_message(
            event.from_user.id,
            f"ℹ️  Мои права доступа в канале {linked_channel} были изменены.\n\n"
            f"Необходимые права:\n"
            f"{message_permissions}\n"
            f"⚠️  <b>Для полноценной работы мне необходимы вышеперечисленные права.\n"
            f"Пожалуйста, дайте необходимый доступ в настройках канала</b>",
            parse_mode="HTML",
        )
        await remove_user_channel(session, event.from_user.id, event.chat.id)
        return

    await bot.send_message(
        event.from_user.id,
        f"ℹ️  Мои права доступа в канале {linked_channel} были изменены.\n\n"
        f"Необходимые права:\n"
        f"{message_permissions}\n"
        "🎉  <b>Все необходимые права выданы!</b>",
        parse_mode="HTML",
    )

    channel = ChannelModel(
        user_id=event.from_user.id,
        chat_id=event.chat.id,
        title=event.chat.title or "Неизвестно",
        username=event.chat.username or "Неизвестно",
    )

    await add_user_channel(session, channel.user_id, channel)
