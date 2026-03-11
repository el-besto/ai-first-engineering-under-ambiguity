"""Main Typer CLI application entry point.

Command groupings:
- llm: Check API keys, available models, and ratelimits.
- health: Ping system services and validate local dependencies.
- graph: Run LangGraph workflows implicitly without API.
- data: Generate and validate synthetic fixture data.
- infra: Evaluate local development stack status.
"""

import typer

from drivers.cli.commands import data, graph, health, infra, llm

# Initialize the main CLI application
app = typer.Typer(
    name="bestow-cli",
    help="Developer CLI Tooling for Bestow LangGraph PoC.",
    add_completion=False,
)

# We will attach command sub-routers here once they are created.
app.add_typer(llm.app, name="llm", help="Commands for LLM and Provider management.")
app.add_typer(health.app, name="health", help="Diagnostics and dependency health checks.")
app.add_typer(graph.app, name="graph", help="LangGraph debugging and execution tools.")
app.add_typer(data.app, name="data", help="Synthetic data generation and validation.")
app.add_typer(infra.app, name="infra", help="Commands for interacting with the local runtime stack.")


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose output",
    ),
) -> None:
    """
    Bestow PoC - Dev CLI Pipeline

    Centralized suite of developer tools to validate, seed, and orchestrate the local environment.
    """
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit(code=0)


if __name__ == "__main__":
    app()
