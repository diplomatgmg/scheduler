__all__ = [
    "BotError",
    "MessageNotAvailableError",
]


class BotError(Exception):
    """Базовая ошибка для исключений в приложении с ботом"""


class MessageNotAvailableError(BotError):
    """Исключение при недоступном Message в CallbackQuery"""

    def __init__(self, text: str | None = None) -> None:
        super().__init__(text or "Message is not available in CallbackQuery")
