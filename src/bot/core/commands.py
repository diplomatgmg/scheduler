from aiogram.types import BotCommand

__all__ = [
    "main_menu_commands",
]

main_menu_commands = [
    BotCommand(command="/start", description="Перезапустить бота"),
]
