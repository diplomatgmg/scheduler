from pydantic_settings import BaseSettings


__all__ = [
    "bot_config",
]


class BotConfig(BaseSettings):
    token: str
    support_username: str

    class Config:
        env_prefix = "BOT_"


bot_config = BotConfig()
