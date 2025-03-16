from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

from bot.core.config import settings
from bot.db.models import Base
from logger import bot_logger

engine = create_async_engine(
    settings.DB.url,
    echo=True,
)

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
)


async def init_db() -> None:
    bot_logger.debug("Инициализация БД")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
