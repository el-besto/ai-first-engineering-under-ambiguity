"""Synthetic Data and Fixture commands."""

import typer

from drivers.cli.utils.console import print_info, print_warning

app = typer.Typer(help="Synthetic data generation and validation.")


@app.command("seed-fixtures")
def seed_fixtures() -> None:
    """Generate synthetic death claim forms via LLM."""
    print_warning("PENDING. Complete once the synthetic-data-plan has been executed.")


@app.command()
def validate() -> None:
    """Validate existing JSON fixtures against domain schemas."""
    print_info("Not implemented: Fixture validation.")
