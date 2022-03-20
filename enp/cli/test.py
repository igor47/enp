from dataclasses import dataclass, field
from functools import partial
from typing import Any, Callable, Dict

import typer
from plumbum import FG, local
from plumbum.commands.processes import ProcessExecutionError

from enp.settings import PROJECT_ROOT


@dataclass(frozen=True)
class Task:
    """Represents a test task"""

    name: str
    should_run: bool
    func: Callable[[], None] = field(repr=False)

    def run(self) -> bool:
        """Runs the task

        Returns:
            bool: whether the task succeeded
        """
        try:
            self.func()  # type: ignore[misc]
            return True
        except typer.Exit:
            return False


app = typer.Typer()


@app.callback()
def main():
    """ENP tests"""
    pass


@app.command()
def all(
    run_black: bool = typer.Option(True, help="Include black in suite run"),
    run_mypy: bool = typer.Option(True, help="Include mypy in suite run"),
    fix: bool = typer.Option(False, help="automagically fix where possible"),
):
    """Runs all tasks in the test suite"""
    tasks = [
        Task("black", run_black, partial(black, fix=fix)),
        Task("mypy", run_mypy, mypy),
    ]

    results: Dict[Task, bool] = {task: task.run() for task in tasks if task.should_run}
    failed = {task for task, result in results.items() if result is False}
    if any(failed):
        typer.echo(typer.style(f"Failed test tasks: {[f.name for f in failed]}", fg="red"))
        raise typer.Exit(1)
    else:
        typer.echo(typer.style(f"All {len(results)} test tasks succeeded!", fg="green"))

@app.command()
def black(fix: bool = typer.Option(False, help="fix errors")):
    """runs black"""
    typer.echo(typer.style("Running black...", fg="yellow"))

    black_opts = []

    if not fix:
        black_opts.append("--check")
    black_opts.append(".")

    # actually run it
    with local.cwd(PROJECT_ROOT):
        try:
            local["black"][black_opts] & FG
            typer.echo(typer.style("black succeeded!", fg="green"))
        except ProcessExecutionError:
            typer.echo(typer.style("black failed!", fg="red"))
            raise typer.Exit(1)


@app.command()
def mypy():
    """runs mypy"""
    typer.echo(typer.style("Running mypy...", fg="yellow"))

    with local.cwd(PROJECT_ROOT):
        try:
            local["mypy"]["--show-error-codes", "."] & FG
            typer.echo(typer.style("mypy succeeded!", fg="green"))
        except ProcessExecutionError:
            typer.echo(typer.style("mypy failed!", fg="red"))
            raise typer.Exit(1)
