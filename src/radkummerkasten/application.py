#!/usr/bin/env python3


"""The application object for radkummerkasten."""


import flask

from .address import Address


__all__ = [
    "create_application",
]


def create_application():
    """Create a new radkummerkasten application."""
    application = flask.Flask(__name__)

    application.register_blueprint(Address())

    return application


if __name__ == "__main__":
    application = create_application()
    application.run()
