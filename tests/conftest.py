#!/usr/bin/env python3


"""Common fixtures and settings for testing radkummerkasten."""


import pytest
import radkummerkasten


@pytest.fixture()
def application():
    """Start a flask application."""
    application = radkummerkasten.create_application()
    yield application


@pytest.fixture()
def client(application):
    """Provide a client for the tests."""
    return application.test_client()


@pytest.fixture()
def runner(application):
    """Provide a cli runner for the tests."""
    return application.test_cli_runner()
