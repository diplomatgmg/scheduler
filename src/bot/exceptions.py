__all__ = ["BotError", "MessageNotAvailableError", "UserNotAvailableError"]


class BotError(Exception):
    """Базовая ошибка для исключений в приложении с ботом"""


class MessageNotAvailableError(BotError):
    """Исключение при недоступном Message в CallbackQuery"""

    def __init__(self, text: str | None = None) -> None:
        super().__init__(text or "Message is not available")


class UserNotAvailableError(BotError):
    """Исключение при недоступном User в CallbackQuery"""

    def __init__(self, text: str | None = None) -> None:
        super().__init__(text or "User is not available")
