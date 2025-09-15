#!/usr/bin/env python3


"""Radkummerkasten frontend."""


import flask

from .address import Address

__all__ = [
    "create_app",
]


def create_app():
    """Create a new radkummerkasten.api application."""
    application = flask.Flask(__name__)

    application.register_blueprint(Address())

    return application
