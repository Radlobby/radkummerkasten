#!/usr/bin/env python3


"""A factory that sets defaults for all radkummerkasten application objects."""


import os

import flask

from .configuration import ProductionConfiguration, TestConfiguration

__all__ = [
    "create_app",
]


def create_app(package_name, instance_path=None):
    """Create a radkummerkasten application."""
    application = flask.Flask(
        package_name,
        instance_path=f"{instance_path}",
        instance_relative_config=True,
    )

    try:
        testing = os.environ["TESTING"]
        if testing.lower() in ["false", "0", "off"]:
            testing = False
        else:
            testing = bool(testing)
    except (AttributeError, KeyError, TypeError):
        testing = False

    if testing:
        application.config.from_object(TestConfiguration)
    else:
        application.config.from_object(ProductionConfiguration)

    application.config.from_pyfile("configuration.py", silent=True)

    return application
