import httpx
import pytest
from sqlalchemy import text

from api.core.config import api_config
from bot.core.config import bot_config
from common.database.engine import get_db_session
from common.redis.config import redis_cache_config
from common.redis.engine import get_redis_instance


@pytest.mark.asyncio
async def test_redis_connection() -> None:
    client = await get_redis_instance(redis_cache_config.connection.dsn)
    pong = await client.ping()

    assert pong is True


@pytest.mark.asyncio
async def test_postgres_connection() -> None:
    async with get_db_session() as session:
        result = await session.execute(text("SELECT 1"))

    scalar_result = result.scalar_one()

    assert scalar_result == 1


@pytest.mark.asyncio
async def test_api_health_check() -> None:
    if not bot_config.use_webhook:
        return

    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://api:{api_config.port}/api/v1/health")

    assert response.status_code == httpx.codes.OK
    assert response.json() == {"status": "healthy"}
