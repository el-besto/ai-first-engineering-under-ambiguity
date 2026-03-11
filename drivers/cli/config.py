"""Shared configuration for the Developer CLI."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class CliSettings(BaseSettings):
    """Configuration specifically for the CLI tools.

    Inherits variables from the main .env file but can be extended
    with CLI-specific overrides if necessary.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    environment: str = "development"
    log_level: str = "INFO"

    # LLM Settings
    openai_api_key: str | None = None
    llm_main_api_key: str | None = None

    # API Settings
    api_url: str = "http://127.0.0.1:8000"


# Global singleton for CLI commands to use
settings = CliSettings()
