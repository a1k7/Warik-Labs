from functools import lru_cache
from pathlib import Path

from pydantic import SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
ENV_FILES = (REPOSITORY_ROOT / ".env.local", REPOSITORY_ROOT / ".env")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILES,
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    app_name: str = "Warik Labs API"
    app_env: str = "development"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    database_url: str = "postgresql+psycopg://warik:warik_dev_only@localhost:5432/warik"
    redis_url: str = "redis://localhost:6379/0"
    cors_origins: str = "http://localhost:3000"
    jwt_secret: SecretStr | None = None
    groq_api_key: SecretStr | None = None
    groq_model: str = "openai/gpt-oss-120b"
    whatsapp_enabled: bool = False
    payments_enabled: bool = False
    live_browser_actions_enabled: bool = False

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @model_validator(mode="after")
    def enforce_production_security(self) -> "Settings":
        if self.app_env.lower() != "production":
            return self

        secret = self.jwt_secret.get_secret_value() if self.jwt_secret else ""
        if len(secret) < 64:
            raise ValueError("Production JWT_SECRET must contain at least 64 characters.")

        if "*" in self.cors_origin_list:
            raise ValueError("Wildcard CORS origins are forbidden in production.")

        if self.payments_enabled:
            raise ValueError("Payments are disabled in this release.")

        if self.live_browser_actions_enabled:
            raise ValueError("Live browser actions are disabled in this release.")

        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
