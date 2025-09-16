#!/usr/bin/env python3


"""Radkummerkasten frontend."""


from .. import factory
from .address import Address

__all__ = [
    "create_app",
]


def create_app():
    """Create a new radkummerkasten.api application."""
    application = factory.create_app(__name__)
    application.register_blueprint(Address())

    return application
