from sqlalchemy import log as sqlalchemy_log
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from common.database.config import db_config
from common.logging.config import log_config
from common.logging.enums import LogLevelSqlalchemyEnum


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

engine = create_async_engine(db_config.url, echo=echo_level.get(log_config.sqlalchemy_level))

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
)
