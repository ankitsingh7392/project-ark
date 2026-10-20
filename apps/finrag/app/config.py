"""Runtime configuration. Every value comes from the environment or `.env`."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str | None = None
    llm_provider: str = "anthropic"
    log_level: str = "info"
    db_health_timeout_s: int = 2


settings = Settings()
