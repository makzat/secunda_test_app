from functools import cache

from pydantic import BaseModel, Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class SecurityConfig(BaseModel):
    api_key_name: str = 'X-API-Key'
    api_key: str = ''


class DatabaseConfig(BaseModel):
    host: str = '127.0.0.1'
    username: str = 'secunda'
    password: str = 'secunda'
    db: str = 'secunda'
    port: int = 5432
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = Field(
        default_factory=lambda: {
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_N_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )

    def get_pg_url(self) -> str:
        url = 'postgresql+asyncpg://{username}:{password}@{host}:{port}/{db}'.format(
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            db=self.db,
        )
        return url


class Settings(BaseSettings):
    run: RunConfig = RunConfig()
    security: SecurityConfig = SecurityConfig()
    db: DatabaseConfig = DatabaseConfig()

    model_config = SettingsConfigDict(
        env_file=['.env', '../.env'],
        env_file_encoding='utf-8',
        frozen=True,
        env_nested_delimiter='__',
        case_sensitive=False,
        extra='ignore',
    )


@cache
def get_settings() -> Settings:
    return Settings()
