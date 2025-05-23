from contextlib import asynccontextmanager

from sqlalchemy import log as sqlalchemy_log
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from collections.abc import AsyncGenerator
from sqlalchemy.exc import SQLAlchemyError

from common.database.config import db_config
from common.logging.config import log_config
from common.logging.enums import LogLevelSqlalchemyEnum


__all__ = [
    "get_db_session",
]


# Предотвращает дублирование логов SQLAlchemy
# https://stackoverflow.com/questions/60804288/pycharm-duplicated-log-for-sqlalchemy-echo-true
sqlalchemy_log._add_default_handler = lambda _: None  # type: ignore[assignment]  # noqa: SLF001

echo_level = {
    LogLevelSqlalchemyEnum.debug: "debug",
    LogLevelSqlalchemyEnum.info: True,
    LogLevelSqlalchemyEnum.warning: None,
}

engine = create_async_engine(db_config.url, echo=echo_level[log_config.sqlalchemy_level])
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession]:
    """Менеджер для работы с сессиями БД"""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError:
            await session.rollback()
            raise
        finally:
            await session.close()
