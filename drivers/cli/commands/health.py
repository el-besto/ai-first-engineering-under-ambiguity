"""Health and Environment validation commands."""

import os
import shutil

import typer

from drivers.cli.config import settings
from drivers.cli.utils.console import print_error, print_info, print_success, print_warning
from drivers.cli.utils.requests import get_with_retry

app = typer.Typer(help="Diagnostics and dependency health checks.")


@app.command()
def api(url: str | None = typer.Option(None, help="Target API URL. Defaults to settings.api_url/health")) -> None:
    """Ping the local FastAPI /health endpoint."""
    target_url = url or f"{settings.api_url.rstrip('/')}/health"
    print_info(f"Pinging {target_url}...")
    try:
        response = get_with_retry(target_url, timeout=3)
        if response.status_code == 200:
            print_success(f"API is healthy! (200 OK) -> {response.json()}")
        else:
            print_warning(f"API responded with status: {response.status_code}")
    except Exception as e:
        print_error(f"Failed to reach API at {target_url}")
        print_error(str(e))
        raise typer.Exit(code=1) from e


@app.command()
def deps() -> None:
    """Verify local environment variables and system dependencies."""
    print_info("Checking essential binaries...")
    binaries = ["uv", "docker", "tilt", "make"]
    missing = False

    for bin_name in binaries:
        if shutil.which(bin_name):
            print_success(f"{bin_name} is installed.")
        else:
            print_error(f"{bin_name} is MISSING from your PATH.")
            missing = True

    print_info("\nChecking environment configuration...")
    if os.path.exists(".env"):
        print_success(".env file exists.")
    else:
        print_error(".env file is MISSING from the project root.")
        missing = True

    if missing:
        print_error("\nSome dependencies or configurations are missing!")
        raise typer.Exit(code=1)
    else:
        print_success("\nAll local dependencies and configurations look good.")
