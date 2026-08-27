from functools import lru_cache
from typing import Literal, Optional
from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from apps.api.app.core.exceptions import AppError


class ConfigurationError(AppError):
    """Typed exception raised when application configuration is missing or invalid."""
    status_code = 500
    code = "CONFIGURATION_ERROR"
    message = "Invalid application configuration."



class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Environment mode (ADR-014: dev vs. viva mode)
    APP_MODE: Literal["dev", "viva", "prod"] = "dev"

    # Server configuration
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    LOG_LEVEL: str = "info"
    API_PORT: int = 8000

    # Database (PostgreSQL)
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "ekcp_dev"
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: int = 5432

    # Cache / Broker (Redis)
    REDIS_URL: str = "redis://redis:6379/0"
    REDIS_PORT: int = 6379

    # Object Storage (MinIO / S3)
    MINIO_ROOT_USER: str = "minioadmin"
    MINIO_ROOT_PASSWORD: str = "minioadmin"
    MINIO_ENDPOINT: str = "http://minio:9000"
    MINIO_PORT: int = 9000
    MINIO_CONSOLE_PORT: int = 9001

    # Web Frontend (React / Vite)
    WEB_PORT: int = 3000
    VITE_API_BASE_URL: str = "http://localhost:8000/api/v1"
    WEB_BUILD_TARGET: str = "runner"

    # Identity & Auth (Phase 3 placeholders)
    JWT_SECRET_KEY: Optional[str] = None
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # AI / LLM Gateway (Phase 8 placeholders — ADR-011)
    GEMINI_API_KEY_1: Optional[str] = None
    GEMINI_API_KEY_2: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None

    @property
    def database_url(self) -> str:
        """Construct PostgreSQL connection string."""
        return (
            f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @model_validator(mode="after")
    def validate_non_dev_security(self) -> "Settings":
        """Enforce strict security validation in viva/prod environments."""
        if self.APP_MODE == "dev":
            # Set dev default for JWT_SECRET_KEY if not explicitly set
            if not self.JWT_SECRET_KEY:
                self.JWT_SECRET_KEY = "dev_secret_key_change_in_production"
            return self

        # In non-dev mode (viva or prod), disallow missing or default secrets
        if not self.JWT_SECRET_KEY or self.JWT_SECRET_KEY == "dev_secret_key_change_in_production":
            raise ConfigurationError(
                f"JWT_SECRET_KEY must be explicitly configured in '{self.APP_MODE}' mode"
            )

        if not self.POSTGRES_PASSWORD or self.POSTGRES_PASSWORD == "postgres":
            raise ConfigurationError(
                f"POSTGRES_PASSWORD cannot use default 'postgres' in '{self.APP_MODE}' mode"
            )

        if not self.MINIO_ROOT_PASSWORD or self.MINIO_ROOT_PASSWORD == "minioadmin":
            raise ConfigurationError(
                f"MINIO_ROOT_PASSWORD cannot use default 'minioadmin' in '{self.APP_MODE}' mode"
            )

        return self


@lru_cache()
def get_settings() -> Settings:
    """Return cached Settings instance."""
    return Settings()


# Export default singleton instance
settings = get_settings()
