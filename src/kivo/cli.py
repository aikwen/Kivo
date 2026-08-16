import typer

from kivo.__about__ import __version__


app = typer.Typer(
    add_completion=False,
    invoke_without_command=True,
)


@app.callback()
def main(ctx: typer.Context) -> None:
    """Start Kivo."""
    if ctx.invoked_subcommand is None:
        from kivo.main import run

        raise typer.Exit(run())


@app.command()
def version() -> None:
    """Show the current Kivo version."""
    typer.echo(__version__)