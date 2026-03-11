"""Local infrastructure control commands."""

import subprocess

import typer

from drivers.cli.utils.console import print_error, print_info, print_success

app = typer.Typer(help="Commands for interacting with the local runtime stack.")


@app.command()
def status() -> None:
    """Check Docker/Tilt status for the local stack."""
    print_info("Checking active Docker containers related to bestow...")
    try:
        result = subprocess.run(
            [
                "docker",
                "ps",
                "--filter",
                "name=bestow",
                "--format",
                "table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Ports}}",
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            if not result.stdout.strip():
                print_info("No local stack containers are currently running.")
            else:
                print_success("Containers found:")
                print(result.stdout)
        else:
            print_error("Failed to execute docker ps.")
            print_error(result.stderr)
    except Exception as e:
        print_error(f"Error checking status: {e}")
        raise typer.Exit(code=1) from e


@app.command()
def clean() -> None:
    """Prune local state and containers using Tilt."""
    print_info("Tearing down local Tilt infrastructure...")
    try:
        result = subprocess.run(["tilt", "down"])
        if result.returncode == 0:
            print_success("Successfully tore down resources.")
        else:
            print_error("Tilt down encountered an error.")
            raise typer.Exit(code=1) from None
    except FileNotFoundError as e:
        print_error("tilt is not installed or not in PATH.")
        raise typer.Exit(code=1) from e
