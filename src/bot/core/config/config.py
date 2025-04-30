from pydantic import BaseModel

from bot.core.config.bot import BotConfig
from bot.core.config.db import DBConfig
from bot.core.config.env import EnvConfig, EnvironmentEnum
from bot.core.config.log import LogConfig
from bot.core.config.sentry import SentrySettings

__all__ = [
    "config",
]


class Config(BaseModel):
    # Окружение подтягивается из .env. Pydantic этого не понимает.
    ENV: EnvConfig = EnvConfig()  # type: ignore[call-arg]
    SENTRY: SentrySettings = SentrySettings()  # type: ignore[call-arg]
    BOT: BotConfig = BotConfig()  # type: ignore[call-arg]
    DB: DBConfig = DBConfig()  # type: ignore[call-arg]
    LOG: LogConfig = LogConfig()  # type: ignore[call-arg]

    class Config:
        env_file = ".env"

    @property
    def debug(self) -> bool:
        return EnvironmentEnum.development == self.ENV.mode


config = Config()
