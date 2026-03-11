"""Shared table formatting utilities for CLI commands.

Uses rich library for beautiful table output with colors.
"""

from rich.console import Console
from rich.table import Table


def create_standard_table(
    title: str,
    columns: list[tuple[str, str, str]],  # (name, justify, style)
    rows: list[list[str]],
) -> Table:
    """Create a rich table for standard CLI outputs.

    Args:
        title: Table title
        columns: List of tuples defining (Header Name, Justification, Style color)
        rows: List of string rows matching the columns length

    Returns:
        Rich Table ready to print
    """
    table = Table(title=title, show_header=True, header_style="bold cyan")

    for name, justify, style in columns:
        table.add_column(name, justify=justify, style=style)  # type: ignore

    for row in rows:
        table.add_row(*row)

    return table


def print_table(table: Table, console: Console | None = None) -> None:
    """Print a rich table to console."""
    if console is None:
        from drivers.cli.utils.console import console as default_console

        console = default_console
    console.print(table)
