import pytest
from apps.api.app.core.config import Settings, ConfigurationError


def test_default_dev_settings(monkeypatch):
    """Verify default dev settings load correctly."""
    monkeypatch.setenv("APP_MODE", "dev")
    monkeypatch.delenv("JWT_SECRET_KEY", raising=False)

    settings = Settings()

    assert settings.APP_MODE == "dev"
    assert settings.APP_PORT == 8000
    assert settings.POSTGRES_USER == "postgres"
    assert settings.POSTGRES_DB == "ekcp_dev"
    assert settings.JWT_SECRET_KEY == "dev_secret_key_change_in_production"
    assert settings.database_url == "postgresql+psycopg://postgres:postgres@postgres:5432/ekcp_dev"


def test_env_var_overrides(monkeypatch):
    """Verify environment variables override default settings."""
    monkeypatch.setenv("APP_MODE", "dev")
    monkeypatch.setenv("POSTGRES_USER", "custom_user")
    monkeypatch.setenv("POSTGRES_DB", "custom_db")
    monkeypatch.setenv("POSTGRES_PORT", "5433")

    settings = Settings()

    assert settings.POSTGRES_USER == "custom_user"
    assert settings.POSTGRES_DB == "custom_db"
    assert settings.POSTGRES_PORT == 5433
    assert settings.database_url == "postgresql+psycopg://custom_user:postgres@postgres:5433/custom_db"


def test_non_dev_default_jwt_secret_raises_error(monkeypatch):
    """Verify non-dev mode fails fast if JWT_SECRET_KEY is missing or uses dev default."""
    monkeypatch.setenv("APP_MODE", "prod")
    monkeypatch.delenv("JWT_SECRET_KEY", raising=False)

    with pytest.raises(ConfigurationError) as exc_info:
        Settings()
    assert "JWT_SECRET_KEY must be explicitly configured" in str(exc_info.value)

    monkeypatch.setenv("JWT_SECRET_KEY", "dev_secret_key_change_in_production")
    with pytest.raises(ConfigurationError) as exc_info:
        Settings()
    assert "JWT_SECRET_KEY must be explicitly configured" in str(exc_info.value)


def test_non_dev_default_postgres_password_raises_error(monkeypatch):
    """Verify non-dev mode fails fast if POSTGRES_PASSWORD uses default 'postgres'."""
    monkeypatch.setenv("APP_MODE", "viva")
    monkeypatch.setenv("JWT_SECRET_KEY", "prod_super_secret_jwt_key")
    monkeypatch.setenv("POSTGRES_PASSWORD", "postgres")

    with pytest.raises(ConfigurationError) as exc_info:
        Settings()
    assert "POSTGRES_PASSWORD cannot use default 'postgres'" in str(exc_info.value)


def test_non_dev_valid_configuration(monkeypatch):
    """Verify non-dev mode succeeds when all security sensitive keys are properly set."""
    monkeypatch.setenv("APP_MODE", "viva")
    monkeypatch.setenv("JWT_SECRET_KEY", "prod_super_secret_jwt_key")
    monkeypatch.setenv("POSTGRES_PASSWORD", "strong_db_password")
    monkeypatch.setenv("MINIO_ROOT_PASSWORD", "strong_minio_password")

    settings = Settings()

    assert settings.APP_MODE == "viva"
    assert settings.JWT_SECRET_KEY == "prod_super_secret_jwt_key"
    assert settings.POSTGRES_PASSWORD == "strong_db_password"
    assert settings.MINIO_ROOT_PASSWORD == "strong_minio_password"
