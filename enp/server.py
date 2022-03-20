import flask

from . import settings


def get_server() -> flask.Flask:
    """Creates a server for this project"""
    server = flask.Flask(__name__, static_folder = settings.STATIC_FOLDER)

    server.add_url_rule('/', endpoint="index", view_func=lambda: server.send_static_file("index.html"))

    return server
