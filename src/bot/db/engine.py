from sqlalchemy import log as sqlalchemy_log
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from bot.core import settings
from bot.core.settings.log import LogLevelSqlalchemyEnum

__all__ = [
    "async_session",
]


# Предотвращает дублирование логов SQLAlchemy
# https://stackoverflow.com/questions/60804288/pycharm-duplicated-log-for-sqlalchemy-echo-true
sqlalchemy_log._add_default_handler = lambda _: None  # type: ignore[assignment]  # noqa: SLF001

echo_level = {
    LogLevelSqlalchemyEnum.debug: "debug",
    LogLevelSqlalchemyEnum.info: True,
    LogLevelSqlalchemyEnum.warning: None,
}

engine = create_async_engine(settings.DB.url, echo=echo_level.get(settings.LOG.sqlalchemy_level))

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
)
