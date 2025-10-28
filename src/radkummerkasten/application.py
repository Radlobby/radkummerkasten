#!/usr/bin/env python3


"""The application object for radkummerkasten."""


import pathlib

from . import api, factory, frontend, tiles

__all__ = [
    "create_app",
]


__MODULE__ = __name__.split(".", maxsplit=1)[0]

DEFAULT_INSTANCE_PATH = (pathlib.Path.cwd() / "instance").absolute()


def create_app(instance_path=DEFAULT_INSTANCE_PATH):
    """Create a new radkummerkasten application."""
    application = factory.create_app(
        __MODULE__,
        instance_path=instance_path,
        static_url_path=None,
        static_folder=None,
    )

    application.register_blueprint(frontend.Radkummerkasten(application.config))
    application.register_blueprint(api.Address(application.config))
    application.register_blueprint(tiles.Tiles(application.config))

    return application
