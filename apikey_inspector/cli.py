import sys
import asyncio
from typing import Optional, List
import typer
from rich.console import Console

from apikey_inspector.inspector import inspect, inspect_batch
from apikey_inspector.formatters.table import create_rich_table
from apikey_inspector.formatters.json_fmt import format_json, format_batch_json

from apikey_inspector import __version__

app = typer.Typer(
    help="Universal API Key Inspector",
    add_completion=False,
    no_args_is_help=True
)
console = Console()

@app.command("version")
def version_cmd():
    """Show the version of apikey-inspector."""
    console.print(f"apikey-inspector v{__version__}")


@app.command("inspect")
def inspect_cmd(
    key: Optional[str] = typer.Argument(None, help="The API key to inspect."),
    from_env: Optional[str] = typer.Option(None, "--from-env", "-e", help="Read key from this environment variable."),
    offline: bool = typer.Option(False, "--offline", help="Only perform regex detection, zero network requests."),
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON instead of table."),
    redact_output: bool = typer.Option(True, "--redact/--no-redact", help="Redact suspected secrets from JSON output."),
    scan: bool = typer.Option(False, "--scan", help="Return exit code 1 if any Valid keys are found (security scanning mode).")
):

    """
    Inspect a single API key safely. Can read from arguments, environment variables, or standard input.
    """
    actual_key = key
    
    # Check for piped input if not provided directly
    if not actual_key and not sys.stdin.isatty():
        actual_key = sys.stdin.read().strip()
        
    if not actual_key and from_env:
        import os
        actual_key = os.environ.get(from_env)
        
    if not actual_key:
        console.print("[red]Error: Must provide a key via argument, stdin, or --from-env.[/red]")
        raise typer.Exit(code=1)

    lines = [line.strip() for line in actual_key.splitlines() if line.strip()]
    if not lines:
        console.print("[red]Error: Provided key is empty.[/red]")
        raise typer.Exit(code=1)
        
    # We use inspect_batch for both single and multiple keys to keep logic simple
    results = asyncio.run(inspect_batch(lines, offline=offline))
    
    if json_output:
        if len(results) == 1:
            console.print(format_json(results[0], redact=redact_output))
        else:
            console.print(format_batch_json(results, redact=redact_output))
    else:
        for res in results:
            console.print(create_rich_table(res))
            console.print()

    # Optional exit logic for security pipelines
    # If any key is VALID and user wants to fail on detection
    if scan and any(r.valid for r in results):
        raise typer.Exit(code=1)



if __name__ == "__main__":
    app()
