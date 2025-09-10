#!/usr/bin/env python3


"""The application object for radkummerkasten."""


import flask

from .address import Address


__all__ = [
    "application",
]


def create_app():
    application = flask.Flask(__name__)
    application.register_blueprint(Address())

    return application


application = create_app()


if __name__ == "__main__":
    application.run()
