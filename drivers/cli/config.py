"""Shared configuration for the Developer CLI."""

from app.config import BaseConfig


class CliSettings(BaseConfig):
    """Configuration specifically for the CLI tools.

    Inherits variables from the main .env file and BaseConfig but can be extended
    with CLI-specific overrides if necessary.
    """

    # LLM Settings
    openai_api_key: str | None = None

    # API Settings
    api_url: str = "http://127.0.0.1:8000"

    # API Settings
    api_url: str = "http://127.0.0.1:8000"


# Global singleton for CLI commands to use
settings = CliSettings()
