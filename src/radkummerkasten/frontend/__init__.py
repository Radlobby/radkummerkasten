#!/usr/bin/env python3


"""Radkummerkasten front end."""


import flask


__all__ = [
    "create_app",
]


def create_app():
    """Create a new radkummerkasten.frontend application."""
    application = flask.Flask(__name__)

    return application
