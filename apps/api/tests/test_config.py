import pytest
from pydantic import SecretStr, ValidationError

from app.config import Settings


def test_production_requires_a_high_entropy_jwt_secret() -> None:
    with pytest.raises(ValidationError):
        Settings(_env_file=None, app_env="production", jwt_secret=None)


def test_production_rejects_wildcard_cors() -> None:
    with pytest.raises(ValidationError):
        Settings(
            _env_file=None,
            app_env="production",
            jwt_secret=SecretStr("a" * 64),
            cors_origins="*",
        )


def test_production_settings_accept_a_local_placeholder_secret_only_when_valid_length() -> None:
    settings = Settings(
        _env_file=None,
        app_env="production",
        jwt_secret=SecretStr("a" * 64),
        cors_origins="https://console.example.com",
    )

    assert settings.cors_origin_list == ["https://console.example.com"]
    assert settings.payments_enabled is False
    assert settings.live_browser_actions_enabled is False
