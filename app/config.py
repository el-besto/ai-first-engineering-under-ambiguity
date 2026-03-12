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
    llm_guardrail_model: str = Field(default="ollama/llama3.1:8b", description="Model to use for PII redaction")
    llm_guardrail_api_base: str = Field(
        default="http://localhost:11434", description="Base URL for the guardrail model"
    )
    llm_guardrail_api_key: str = Field(default="local-dev", repr=False, description="API key for the guardrail model")
    llm_guardrail_secret_key: str | None = Field(
        default=None, repr=False, description="32-byte secret key for vaultless AES-GCM PII encryption"
    )

    # LangSmith Configuration
    langsmith_tracing: bool = Field(default=False, description="Enable LangSmith tracing")
    langsmith_api_key: str | None = Field(default=None, repr=False, description="API key for LangSmith")
    langchain_project: str | None = Field(default=None, description="Project name for LangSmith")
