from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


__all__ = [
    "db_config",
]


class DBConfig(BaseSettings):
    user: str
    password: SecretStr
    host: str
    port: int = Field(ge=1, le=65535)
    name: str

    model_config = SettingsConfigDict(env_prefix="DB_")

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


db_config = DBConfig()
