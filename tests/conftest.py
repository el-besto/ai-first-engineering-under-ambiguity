import os

import pytest
import structlog

from app.infrastructure.telemetry.logger import clear_context, configure_logging


@pytest.fixture(autouse=True, scope="session")
def setup_test_logging():
    """
    Automatically hooks structlog into the testing environment for the session.
    Sets the environment explicitly to 'testing' so configurations are deterministic
    and pytest's stdout/stderr capture mechanism properly silences passing tests.
    """
    os.environ["ENVIRONMENT"] = "testing"
    configure_logging(environment="testing", log_level="INFO", log_format="console")


@pytest.fixture(autouse=True)
def clear_structlog_contextvars():
    """
    Ensure each test gets a clean slate for structlog thread-local context variables
    like session_id or trace_id.
    """
    clear_context()
    yield
    clear_context()


@pytest.fixture
def log_capture():
    """
    Provides a way to capture structlog events in memory for test assertions.
    Usage:
        def test_something(log_capture):
            # ... do something ...
            assert {"event": "my_event", "log_level": "info"} in log_capture
    """
    # Note: If tests explicitly need to assert on logs, they can use this fixture.
    # We yield a list that structlog.testing.LogCapture() populates.

    # We temporarily reconfigure structlog to just capture events
    original_processors = structlog.get_config()["processors"]
    capture = structlog.testing.LogCapture()
    structlog.configure(processors=[capture])

    yield capture.entries

    # Restore standard configuration
    structlog.configure(processors=original_processors)
