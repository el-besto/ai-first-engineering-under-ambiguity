"""Console utilities for CLI commands.

Provides type-safe wrappers for Rich Console output.
"""

from rich.console import Console

# Standard console for normal output
console = Console()

# Error console that writes to stderr
error_console = Console(stderr=True, style="bold red")

# Success console
success_console = Console(style="bold green")


def print_error(message: str) -> None:
    """Print error message to stderr with red styling."""
    error_console.print(f"❌ {message}")


def print_warning(message: str) -> None:
    """Print warning message with yellow styling."""
    console.print(f"[yellow]⚠️  {message}[/yellow]")


def print_success(message: str) -> None:
    """Print success message with green styling."""
    success_console.print(f"✅ {message}")


def print_info(message: str) -> None:
    """Print informational message."""
    console.print(message)
