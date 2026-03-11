"""HTTP and Request utilities for CLI commands.

Provides robust Wrappers around httpx using Tenacity for standard retries.
"""

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from drivers.cli.utils.console import print_warning


def log_retry_attempt(retry_state):
    """Log a warning when an HTTP request is retried."""
    if retry_state.attempt_number > 1:
        print_warning(f"Retrying request... (Attempt {retry_state.attempt_number})")


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    before=log_retry_attempt,
    reraise=True,
)
def get_with_retry(url: str, params: dict | None = None, timeout: int = 5) -> httpx.Response:
    """Perform a synchronous HTTP GET request with exponential backoff retries.

    Useful for checking local system health or external APIs that might be flaky.
    """
    with httpx.Client(timeout=timeout) as client:
        response = client.get(url, params=params)
        response.raise_for_status()
        return response


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    before=log_retry_attempt,
    reraise=True,
)
async def async_get_with_retry(url: str, params: dict | None = None, timeout: int = 5) -> httpx.Response:
    """Perform an asynchronous HTTP GET request with exponential backoff retries."""
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response
