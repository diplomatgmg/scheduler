from aiogram.types import InlineKeyboardButton, Message
from pydantic import BaseModel

from common.schemas.url import HttpsUrl


__all__ = [
    "PostContext",
    "PreviewMessageContext",
    "UrlButton",
]


class UrlButton(BaseModel):
    text: str
    url: HttpsUrl


class PreviewMessageContext(BaseModel):
    message: Message
    buttons: list[list[InlineKeyboardButton]] | None = None


class PostContext(BaseModel):
    selected_channel_chat_id: int
    selected_channel_title: str
    selected_channel_username: str | None
    preview_message: PreviewMessageContext | None = None
