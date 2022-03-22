import signal
import sys

import typer
from plumbum import BG, FG, local
from plumbum.commands.processes import ProcessExecutionError

from enp.settings import PROJECT_ROOT


app = typer.Typer()


@app.callback()
def main():
    """ENP tests"""
    pass


@app.command()
def flask():
    """runs the backend dev server"""
    from enp.server import get_server
    server = get_server()

    typer.echo("Starting flask dev server...")
    server.run(debug=True)

@app.command()
def dev():
    """Runs all tasks in the test suite"""
    with local.cwd(PROJECT_ROOT):
        # start the vite dev server. it will proxy to the flask server
        typer.echo("Starting vite dev server...")
        vite_cmd = local["npm"]["exec", "vite", "serve"]
        vite_process = vite_cmd & BG(stdout=sys.stdout, stderr=sys.stderr)

        # now start the flask server
        flask_cmd = local["enp"]["run", "flask"]
        try:
            flask_cmd & FG
        finally:
            vite_process.proc.send_signal(signal.SIGINT)
            exit_code = vite_process.proc.wait(timeout=1)
            typer.echo(f"Vite exited with code {exit_code}")

@app.command()
def build():
    """Runs the vite build process to produce finished build artifact"""
    local["npm"]["exec", "vite", "build"] & FG

@app.command()
def prod():
    """Production version of the flask server"""
    from enp.server import get_server
    server = get_server(prod = True)

    typer.echo("Starting flask dev server...")
    server.run()


