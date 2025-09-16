#!/usr/bin/env python3


"""The application object for radkummerkasten."""


import pathlib

import werkzeug.middleware.dispatcher

from . import api, factory, frontend, tiles

__all__ = [
    "create_app",
]


__MODULE__ = __name__.split(".", maxsplit=1)[0]

DEFAULT_INSTANCE_PATH = (pathlib.Path.cwd() / "instance").absolute()


def create_app(instance_path=DEFAULT_INSTANCE_PATH):
    """Create a new radkummerkasten application."""
    application = factory.create_app(__MODULE__, instance_path=instance_path)
    application.wsgi_app = werkzeug.middleware.dispatcher.DispatcherMiddleware(
        frontend.create_app(instance_path),
        {
            "/api": api.create_app(instance_path),
            "/tiles": tiles.create_app(instance_path),
        },
    )
    return application
