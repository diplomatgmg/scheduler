from typing import Annotated

from fastapi import APIRouter, Header, HTTPException, Request
from loguru import logger

from api.endpoints.v1.schemas.webhook import WebhookResponse
from bot.core.config import bot_config
from common.redis.client import RedisQueueClient
from common.redis.enums import RedisCacheKeyEnum


__all__ = [
    "router",
]


router = APIRouter()


@router.post("", summary="Webhook для получения updates Telegram")
async def telegram_webhook(
    request: Request,
    x_telegram_bot_api_secret_token: Annotated[str | None, Header()] = None,
) -> WebhookResponse:
    if x_telegram_bot_api_secret_token != bot_config.webhook_token:
        logger.error("Bot token is invalid")
        raise HTTPException(403, "Invalid bot token")

    data = await request.json()
    client = RedisQueueClient()
    await client.push(RedisCacheKeyEnum.TELEGRAM_UPDATES, data)

    return WebhookResponse()
