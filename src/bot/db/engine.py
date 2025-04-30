from sqlalchemy import log as sqlalchemy_log
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from bot.core import config
from bot.core.config.log import LogLevelSqlalchemyEnum

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

engine = create_async_engine(config.DB.url, echo=echo_level.get(config.LOG.sqlalchemy_level))

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
)

# FIXME Думаю, лучше вынести бд в src/database
