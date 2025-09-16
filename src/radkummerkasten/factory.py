#!/usr/bin/env python3


"""A factory that sets defaults for all radkummerkasten application objects."""


import flask

__all__ = [
    "create_app",
]


def create_app(package_name, instance_path=None):
    """Create a radkummerkasten application."""
    application = flask.Flask(
        package_name,
        instance_path=instance_path,
        instance_relative_config=True,
    )
    application.config.from_object("radkummerkasten.configuration.DefaultConfiguration")
    application.config.from_pyfile("configuration.Configuration")
    return application
