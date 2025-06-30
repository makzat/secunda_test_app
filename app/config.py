from functools import cache

from pydantic import BaseModel, Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class DatabaseConfig(BaseModel):
    url: str = "postgresql+asyncpg://exchange_service:exchange_service@localhost:5432/exchange_service"
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = Field(
        default_factory={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_N_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )


class SourceRateUrl(BaseModel):
    source_russian_bank: str = "https://cbr.ru/scripts/XML_daily.asp"


class Settings(BaseSettings):
    run: RunConfig = RunConfig()
    db: DatabaseConfig = DatabaseConfig()
    source_url: SourceRateUrl = SourceRateUrl()

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        frozen=True,
        env_nested_delimiter='__',
        case_sensitive=False,
        extra='ignore',
    )


@cache
def get_settings() -> Settings:
    return Settings()
