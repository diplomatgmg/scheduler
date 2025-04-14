from pydantic import BaseModel

from bot.core.settings.bot import BotSettings
from bot.core.settings.db import DBSettings
from bot.core.settings.env import EnvironmentEnum, EnvSettings
from bot.core.settings.log import LogSettings
from bot.core.settings.sentry import SentrySettings

__all__ = [
    "settings",
]


class Settings(BaseModel):
    ENV: EnvSettings = EnvSettings()  # type: ignore[call-arg]
    SENTRY: SentrySettings = SentrySettings()  # type: ignore[call-arg]
    BOT: BotSettings = BotSettings()  # type: ignore[call-arg]
    DB: DBSettings = DBSettings()  # type: ignore[call-arg]
    LOG: LogSettings = LogSettings()  # type: ignore[call-arg]

    class Config:
        env_file = ".env"

    @property
    def debug(self) -> bool:
        return EnvironmentEnum.development == self.ENV.mode


settings = Settings()
