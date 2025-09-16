#!/usr/bin/env python3


"""Radkummerkasten front end."""


import flask

__all__ = [
    "create_app",
]


def create_app(instance_path):
    """Create a new radkummerkasten.frontend application."""
    application = flask.Flask(
        __name__,
        instance_path,
        instance_relative_config=True,
    )

    return application
