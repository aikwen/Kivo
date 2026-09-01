import typer

from kivo.__about__ import __version__
from kivo.setup.windows import run, setup as setup_windows
from kivo.utils.platform import is_windows


app = typer.Typer(
    add_completion=False,
    invoke_without_command=True,
)


@app.callback()
def main(ctx: typer.Context) -> None:
    """Start Kivo."""
    if ctx.invoked_subcommand is None:
        if not is_windows():
            raise RuntimeError(
                "Kivo currently supports Windows only."
            )

        run()


@app.command()
def setup(
    reset: bool = typer.Option(
        False,
        "--reset",
        help="Reset Kivo configuration to defaults.",
    ),
) -> None:
    """Set up Kivo."""
    if not is_windows():
        raise RuntimeError(
            "Kivo currently supports Windows only."
        )

    setup_windows(
        reset=reset,
    )


@app.command()
def version() -> None:
    """Show the current Kivo version."""
    typer.echo(__version__)