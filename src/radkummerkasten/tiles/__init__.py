#!/usr/bin/env python3


"""Map tiles for radkummerkasten."""


import flask

from .tiles import Tiles

__all__ = [
    "create_app",
]


def create_app():
    """Create a new radkummerkasten.tiles application."""
    application = flask.Flask(__name__)

    application.register_blueprint(Tiles())

    return application
