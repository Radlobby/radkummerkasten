#!/usr/bin/env python3


"""Map tiles for radkummerkasten."""


from .. import factory
from .tiles import Tiles

__all__ = [
    "create_app",
]


def create_app():
    """Create a new radkummerkasten.tiles application."""
    application = factory.create_app(__name__)
    application.register_blueprint(Tiles())

    return application
