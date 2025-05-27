from aiogram.types import Message
from pydantic import BaseModel

from common.schemas.url import HttpsUrl


__all__ = [
    "PostContext",
    "UrlButton",
]


class PostContext(BaseModel):
    selected_channel_chat_id: int
    selected_channel_title: str
    selected_channel_username: str | None

    preview_message: Message | None = None


class UrlButton(BaseModel):
    text: str
    url: HttpsUrl
