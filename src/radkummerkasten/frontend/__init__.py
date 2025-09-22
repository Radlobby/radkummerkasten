#!/usr/bin/env python3


"""Radkummerkasten front end."""

from .. import factory
from .radkummerkasten import Radkummerkasten

__all__ = [
    "create_app",
]


def create_app(instance_path):
    """Create a new radkummerkasten.frontend application."""
    application = factory.create_app(__name__, instance_path)
    application.register_blueprint(Radkummerkasten())
    return application
