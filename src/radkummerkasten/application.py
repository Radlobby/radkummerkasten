#!/usr/bin/env python3


"""The application object for radkummerkasten."""


import flask
import werkzeug.middleware.dispatcher

from . import api, frontend, tiles

__all__ = [
    "create_app",
]


__MODULE__ = __name__.split(".")[0]


def create_app(instance_path=None):
    """Create a new radkummerkasten application."""
    application = flask.Flask(
        __MODULE__,
        instance_path=instance_path,
        instance_relative_config=True,
    )
    application.wsgi_app = werkzeug.middleware.dispatcher.DispatcherMiddleware(
        frontend.create_app(),
        {
            "/api": api.create_app(instance_path),
            "/tiles": tiles.create_app(instance_path),
        },
    )
    return application


if __name__ == "__main__":
    application = create_app()
    application.run()
