from loguru import logger
from sqlalchemy import log as sqlalchemy_log
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from bot.core.config import settings
from bot.db.models import Base

# Предотвращает дублирование логов SQLAlchemy
# https://stackoverflow.com/questions/60804288/pycharm-duplicated-log-for-sqlalchemy-echo-true
sqlalchemy_log._add_default_handler = lambda _: None  # type: ignore[assignment]  # noqa: SLF001


engine = create_async_engine(settings.DB.url, echo=True)

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
)


async def init_db() -> None:
    logger.debug("Инициализация БД")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
