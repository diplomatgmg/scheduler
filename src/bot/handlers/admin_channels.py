from aiogram import Router
from aiogram.filters import (
    ADMINISTRATOR,
    PROMOTED_TRANSITION,
    ChatMemberUpdatedFilter,
)
from aiogram.types import ChatMemberAdministrator, ChatMemberUpdated
from loguru import logger

from bot.core.loader import bot
from bot.utils.user import get_username

__all__ = ()

router = Router(name="admin_channels")


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=PROMOTED_TRANSITION))
async def on_bot_promoted(event: ChatMemberUpdated) -> None:
    chat_username = get_username(event)
    username = get_username(event.from_user)
    logger.debug(f"Bot was promoted to administrator by user {username} in the channel {chat_username}")

    await bot.send_message(
        event.from_user.id,
        f"Вы добавили меня в администраторы канала {chat_username}\n\n",
    )

    await on_bot_permissions_changed(event)


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=~PROMOTED_TRANSITION))
async def on_bot_demoted(event: ChatMemberUpdated) -> None:
    chat_username = get_username(event)
    username = get_username(event.from_user)
    logger.debug(f"Bot was removed from administrators by user {username} in channel {chat_username}")

    await bot.send_message(
        event.from_user.id,
        f"Я больше не администратор в канале {chat_username}\n\n"
        f"<b>Теперь я не смогу управлять постами в канале</b>",
        parse_mode="HTML",
    )


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=ADMINISTRATOR))
async def on_bot_permissions_changed(event: ChatMemberUpdated) -> None:
    chat_username = get_username(event)
    username = get_username(event.from_user)
    logger.debug(f"Bot permissions were updated by user {username} in channel {chat_username}")

    permissions: ChatMemberAdministrator = await bot.get_chat_member(event.chat.id, bot.id)  # type: ignore[assignment]

    permissions_list = (
        (permissions.can_post_messages, "Могу отправлять сообщения в канал"),
        (permissions.can_delete_messages, "Могу удалять сообщения в канале"),
    )

    message_permissions = ""
    all_granted = True

    for has_permission, description in permissions_list:
        emoji = "✅" if has_permission else "❌"
        message_permissions += f"    {emoji} {description}\n"
        if not has_permission:
            all_granted = False

    if all_granted:
        await bot.send_message(
            event.from_user.id,
            f"Мои права доступа в канале {chat_username} были изменены.\n\n"
            f"Необходимые права:\n"
            f"{message_permissions}\n"
            "<b>Все необходимые права выданы!</b>",
            parse_mode="HTML",
        )
    else:
        await bot.send_message(
            event.from_user.id,
            f"Мои права доступа в канале {chat_username} были изменены.\n\n"
            f"Необходимые права:\n"
            f"{message_permissions}\n"
            f"<b>Для полноценной работы мне необходимы вышеперечисленные права.\n"
            f"Пожалуйста, дайте необходимый доступ в настройках канала</b>",
            parse_mode="HTML",
        )
