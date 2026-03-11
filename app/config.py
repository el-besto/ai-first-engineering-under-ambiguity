from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    """
    Base configuration class for the application.
    Loaded via pydantic-settings which defaults to checking the environment
    and optionally a .env file.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    environment: str = "development"
    log_level: str = "INFO"
    log_format: str = "auto"

    # Live Model Provider Configuration
    llm_main_model: str | None = Field(default=None, description="Main model for application logic")
    llm_main_api_key: str | None = Field(default=None, repr=False, description="API key for the main model")
    llm_main_api_base: str | None = Field(default=None, description="Base URL for the main model (if applicable)")
    llm_main_requests_per_minute: float | None = Field(
        default=60.0, description="Rate limit (requests per minute) for the main model"
    )

    # (Stretch Goal) Local SLM for PII Guardrail
    llm_guardrail_model: str | None = Field(default=None, description="Model to use for PII redaction")
    llm_guardrail_api_base: str | None = Field(default=None, description="Base URL for the guardrail model")
    llm_guardrail_api_key: str | None = Field(default=None, repr=False, description="API key for the guardrail model")
