import flask

from . import settings
from .api import api


def get_server(prod: bool = False) -> flask.Flask:
    """Creates a server for this project"""
    server = flask.Flask(__name__, static_folder=settings.ASSETS_PATH)

    # static routes only exist in prod mode
    if prod:
        server.add_url_rule(
            "/", endpoint="index", view_func=lambda: flask.send_file(settings.INDEX_PATH)
        )

    server.register_blueprint(api, url_prefix="/api")

    return server
