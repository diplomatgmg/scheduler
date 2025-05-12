import pytest

from common.redis.engine import get_redis_instance


@pytest.mark.asyncio
async def test_redis_connection() -> None:
    client = await get_redis_instance()
    pong = await client.ping()
    assert pong is True
