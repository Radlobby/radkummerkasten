#!/usr/bin/env python3


"""The application object for radkummerkasten."""


import flask
import werkzeug.middleware.dispatcher

from . import api, frontend, tiles

__all__ = [
    "create_app",
]


def create_app():
    """Create a new radkummerkasten application."""
    application = flask.Flask(__name__)
    application.wsgi_app = werkzeug.middleware.dispatcher.DispatcherMiddleware(
        frontend.create_app(),
        {
            "/api": api.create_app(),
            "/tiles": tiles.create_app(),
        },
    )
    return application


if __name__ == "__main__":
    application = create_app()
    application.run()
