from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import BaseSettings
from sqlalchemy import URL

from bot.core.enums import EnvironmentEnum, LogLevelEnum, LogLevelSqlalchemyEnum

__all__ = [
    "settings",
]


class EnvSettings(BaseSettings):
    mode: EnvironmentEnum

    class Config:
        env_prefix = "ENV_"


class DBSettings(BaseSettings):
    user: str
    password: SecretStr
    host: str
    port: int = Field(ge=1, le=65535)
    name: str

    class Config:
        env_prefix = "DB_"

    @property
    def url(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.user,
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            database=self.name,
        )


class BotSettings(BaseSettings):
    token: str

    class Config:
        env_prefix = "BOT_"


class LogSettings(BaseSettings):
    level: LogLevelEnum
    sqlalchemy_level: LogLevelSqlalchemyEnum

    class Config:
        env_prefix = "LOG_"


class Settings(BaseModel):
    ENV: EnvSettings = EnvSettings()  # type: ignore[call-arg]
    BOT: BotSettings = BotSettings()  # type: ignore[call-arg]
    DB: DBSettings = DBSettings()  # type: ignore[call-arg]
    LOG: LogSettings = LogSettings()  # type: ignore[call-arg]

    class Config:
        env_file = ".env"

    @property
    def debug(self) -> bool:
        return EnvironmentEnum.development == self.ENV


settings = Settings()
