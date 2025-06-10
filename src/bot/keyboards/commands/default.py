from aiogram.types import BotCommand

from bot.keyboards.commands.enums import DefaultCommandEnum


__all__ = [
    "default_commands",
]


default_commands = [
    BotCommand(command=DefaultCommandEnum.START, description="Перезапустить бота"),
    BotCommand(command=DefaultCommandEnum.SET_TIMEZONE, description="Изменить временную зону"),
    BotCommand(command=DefaultCommandEnum.SUPPORT, description="Обратная связь"),
]
