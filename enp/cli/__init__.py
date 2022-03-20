from typing import Optional

import typer

from enp.version import get_package_version
from enp.cli.test import app as test_app

app = typer.Typer()
app.add_typer(test_app, name="tests")


def show_version(should: bool):
    """shows the version and exits"""
    if should:
        typer.echo(get_package_version())
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        callback=show_version,
        is_eager=True,
        help="Show version and exit",
    )
) -> None:
    """Evergrow Number Printer"""
    pass
