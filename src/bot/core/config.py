import re
from urllib.parse import urljoin

from pydantic import field_validator
from pydantic_settings import BaseSettings

from common.schemas.url import HttpsUrl


__all__ = [
    "bot_config",
]


class BotConfig(BaseSettings):
    token: str
    support_username: str
    use_webhook: bool
    webhook_host: HttpsUrl
    webhook_path: str
    webhook_token: str

    class Config:
        env_prefix = "BOT_"

    @property
    def webhook_url(self) -> HttpsUrl:
        return HttpsUrl(urljoin(str(self.webhook_host), self.webhook_path))

    @field_validator("webhook_path", mode="before")
    @classmethod
    def validate_webhook_path(cls, value: str) -> str:
        if not value.startswith("/"):
            msg = 'Путь должен начинаться на "/"'
            raise ValueError(msg)
        if value.endswith("/"):
            msg = 'Путь не должен заканчиваться на "/"'
            raise ValueError(msg)
        return value

    @field_validator("webhook_token", mode="before")
    @classmethod
    def validate_webhook_token(cls, value: str) -> str:
        min_token_length = 1
        max_token_length = 256

        if not (min_token_length <= len(value) <= max_token_length):
            msg = f"webhook_token должен содержать от {min_token_length} до {max_token_length} символов"
            raise ValueError(msg)
        if not re.fullmatch(r"[A-Za-z0-9_-]+", value):
            msg = 'webhook_token может содержать только "A-Z", "a-z", "_", "-"'
            raise ValueError(msg)
        return value


bot_config = BotConfig()
