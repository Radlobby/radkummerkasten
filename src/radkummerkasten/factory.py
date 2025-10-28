#!/usr/bin/env python3


"""A factory that sets defaults for all radkummerkasten application objects."""


import os
import pathlib

import flask

from .configuration import ProductionConfiguration, TestConfiguration

__all__ = [
    "create_app",
]


def create_app(package_name, instance_path, *args, **kwargs):
    """Create a radkummerkasten application."""
    instance_path = pathlib.Path(instance_path).resolve()
    application = flask.Flask(
        package_name,
        *args,
        instance_path=f"{instance_path}",
        instance_relative_config=True,
        **kwargs,
    )

    try:
        testing = os.environ["TESTING"]
        if testing.lower() in ["false", "0", "off", ""]:
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
