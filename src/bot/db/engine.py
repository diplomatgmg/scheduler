from loguru import logger
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

from bot.core.config import settings
from bot.db.models import Base

# Предотвращает дублирование логов SQLAlchemy
# https://stackoverflow.com/questions/60804288/pycharm-duplicated-log-for-sqlalchemy-echo-true
# sqlalchemy_log._add_default_handler = lambda _: None  # type: ignore


engine = create_async_engine(settings.DB.url)

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
)


async def init_db() -> None:
    logger.debug("Инициализация БД")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
