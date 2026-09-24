from functools import lru_cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "PrimeHomes Real Estate Lead Bot"
    app_version: str = "0.1.0"
    app_env: str = "development"
    debug: bool = False
    log_level: str = "INFO"
    api_v1_prefix: str = "/api/v1"
    cors_origins: str = "http://localhost:5173"
    database_url: str = "sqlite+pysqlite:///:memory:"

    n8n_enabled: bool = False
    n8n_webhook_url: str = (
        "http://localhost:5678/webhook/lead-intake-v1"
    )
    n8n_webhook_token: SecretStr | None = None
    n8n_timeout_seconds: float = Field(default=5.0, gt=0, le=30)

    ai_enabled: bool = False
    ai_endpoint_url: str = (
        "https://api.openai.com/v1/chat/completions"
    )
    ai_api_key: SecretStr | None = None
    ai_model: str | None = None
    ai_timeout_seconds: float = Field(default=15.0, gt=0, le=60)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def cors_origins_list(self) -> list[str]:
        return [
            value.strip()
            for value in self.cors_origins.split(",")
            if value.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
