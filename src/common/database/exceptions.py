from sqlalchemy.exc import SQLAlchemyError


__all__ = ["UserDoesNotExistError"]


class UserDoesNotExistError(SQLAlchemyError):
    """Исключение, выбрасываемое при попытке получить пользователя, который не существует в базе данных."""

    def __init__(self, text: str | None = None) -> None:
        super().__init__(text or "User does not exist")
