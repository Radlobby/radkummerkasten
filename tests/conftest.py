#!/usr/bin/env python3


"""Common fixtures and settings for testing radkummerkasten."""

import os
import pathlib

import pytest

import radkummerkasten

SOME_ONLINE_FILE_URL = (
    "https://github.com/christophfink/radkummerkasten.at/blob/main/LICENSE"
)
TEST_DATA_DIRECTORY = (pathlib.Path(__file__).parent / "data").absolute()


@pytest.fixture(scope="session")
def application():
    """Start a flask application."""
    instance_path = TEST_DATA_DIRECTORY
    os.environ["TESTING"] = "TRUE"
    application = radkummerkasten.create_app(instance_path)
    yield application


@pytest.fixture()
def client(application):
    """Provide a client for the tests."""
    return application.test_client()


@pytest.fixture()
def runner(application):
    """Provide a cli runner for the tests."""
    return application.test_cli_runner()


@pytest.fixture()
def some_online_file_url():
    """Return the URL of a random online file."""
    yield SOME_ONLINE_FILE_URL
