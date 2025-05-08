from pydantic import HttpUrl
from pydantic_settings import BaseSettings


__all__ = [
    "bot_config",
]


class BotConfig(BaseSettings):
    token: str
    support_username: str

    webhook_url: HttpUrl
    webhook_path: str

    class Config:
        env_prefix = "BOT_"


bot_config = BotConfig()
