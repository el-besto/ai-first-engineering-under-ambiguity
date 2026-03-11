"""Local infrastructure control commands."""

import os
import secrets
import subprocess

import dotenv
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


@app.command("generate-guardrail-key")
def generate_guardrail_key() -> None:
    """Generate a random 32-byte hex key for Vaultless Guardrail and write it to .env."""
    print_info("Generating a new 32-byte secret key for the PII guardrail...")

    # Generate 64 hex characters (32 bytes)
    secret_key = secrets.token_hex(32)

    # Locate the .env file in the project root
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    env_path = os.path.join(root_dir, ".env")

    if not os.path.exists(env_path):
        print_info(f".env file not found at {env_path}. Creating a new one...")
        open(env_path, "a").close()

    print_info("Updating .env file with LLM_GUARDRAIL_SECRET_KEY...")
    try:
        # Use python-dotenv to set the key safely
        dotenv.set_key(env_path, "LLM_GUARDRAIL_SECRET_KEY", secret_key)
        print_success("Key successfully generated and saved to .env!")
        print_success(f"Key: {secret_key}")
    except Exception as e:
        print_error(f"Failed to update .env file: {e}")
        raise typer.Exit(code=1) from e
