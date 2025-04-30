from aiogram.types import BotCommand

__all__ = [
    "default_commands",
]

default_commands = [
    BotCommand(command="/start", description="Перезапустить бота"),
    BotCommand(command="/support", description="Обратная связь"),
]
