import typer
from plumbum import FG, local
from plumbum.commands.processes import ProcessExecutionError

from enp.settings import PROJECT_ROOT


app = typer.Typer()


@app.callback()
def main():
    """ENP tests"""
    pass


@app.command()
def dev():
    """Runs all tasks in the test suite"""
    import enp.server as srv
    server = srv.get_server()

    server.run(debug=True)
