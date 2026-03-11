"""
Centralized structured logging with structlog.
"""

import logging
import sys
import traceback
from typing import Any

import structlog
from pythonjsonlogger.jsonlogger import JsonFormatter  # type: ignore[attr-defined]


def _add_emoji_prefix(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
    """Add emoji prefix to event name in development mode for better visual scanning."""
    event = event_dict.get("event", "")
    if not event:
        return event_dict

    # Emoji mapping (order matters - most specific first)
    emoji_map = [
        (["failed", "error", "exception"], "❌"),
        (["warning", "degraded"], "⚠️"),
        (["completed", "success"], "✅"),
        (["started"], "🚀"),
        (["dspy", "llm", "generation", "extraction"], "🧠"),
        (["database", "query", "sql", "postgres", "weaviate"], "💾"),
        (["api", "http", "request", "response"], "🌐"),
        (["blob", "file", "download", "upload", "ocr"], "📄"),
        (["search", "retrieval", "similar"], "🔍"),
    ]

    event_lower = event.lower()
    for keywords, emoji in emoji_map:
        if any(keyword in event_lower for keyword in keywords):
            event_dict["event"] = f"{emoji} {event}"
            break

    return event_dict


def _configure_stdlib_logging(log_level: str, format_json: bool = False) -> None:
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    root_logger.handlers.clear()

    # Suppress noisy third-party library logs
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level.upper()))

    if format_json:
        json_formatter = JsonFormatter(
            "%(timestamp)s %(level)s %(name)s %(message)s",
            rename_fields={"levelname": "level", "name": "logger"},
            timestamp=True,
        )
        console_handler.setFormatter(json_formatter)
    else:
        console_handler.setFormatter(logging.Formatter("%(message)s"))

    root_logger.addHandler(console_handler)


def configure_logging(
    log_level: str = "INFO",
    log_format: str = "auto",
    environment: str = "development",
) -> None:
    format_json = False
    if log_format == "auto":
        format_json = environment in ("qa", "staging", "production")
    elif log_format == "json":
        format_json = True

    _configure_stdlib_logging(log_level=log_level, format_json=False)

    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
    ]

    if environment in ("development", "local") and not format_json:
        shared_processors.append(_add_emoji_prefix)

    if format_json:
        processors = [
            *shared_processors,
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer(),
        ]
    else:
        processors = [
            *shared_processors,
            structlog.dev.set_exc_info,
            structlog.dev.ConsoleRenderer(colors=True),
        ]

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    return structlog.get_logger(name)


def bind_context(**kwargs: Any) -> None:
    structlog.contextvars.bind_contextvars(**kwargs)


def clear_context() -> None:
    structlog.contextvars.clear_contextvars()


def log_exception(
    logger: structlog.stdlib.BoundLogger, event: str, exc: Exception, **extra_context: Any
) -> None:
    logger.error(
        event,
        **{
            "error.type": type(exc).__name__,
            "error.message": str(exc),
            "exception.stacktrace": traceback.format_exc(),
            **extra_context,
        },
    )
