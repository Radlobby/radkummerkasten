#!/usr/bin/env python3


"""Common fixtures and settings for testing radkummerkasten."""

import os
import pathlib
import tempfile

import pytest

import radkummerkasten

from .local_server import LocalServer

SOME_ONLINE_FILE_URL = (
    "https://github.com/christophfink/radkummerkasten.at/blob/main/LICENSE"
)
TEST_DATA_DIRECTORY = (pathlib.Path(__file__).parent / "data").absolute()
TEST_INSTANCE_DIRECTORY = (pathlib.Path(__file__).parent / "instance").absolute()


@pytest.fixture(scope="session")
def application(test_instance_directory):
    """Start a flask application."""
    os.environ["TESTING"] = "TRUE"
    application = radkummerkasten.create_app(instance_path=test_instance_directory)
    del os.environ["TESTING"]
    yield application


@pytest.fixture(scope="session")
def application_with_empty_config():
    """Start a flask application."""
    with tempfile.TemporaryDirectory() as instance_path:
        os.environ["TESTING"] = "TRUE"
        application = radkummerkasten.create_app(instance_path)
        del os.environ["TESTING"]
        yield application


@pytest.fixture(scope="session")
def client(application):
    """Provide a client for the tests."""
    return application.test_client()


@pytest.fixture(scope="function")
def expected_tile_pbf(request, test_data_directory):
    """Read the expected content of a vector tile from disk."""
    with (test_data_directory / f"{request.param}.pbf").open("rb") as f:
        tile_pbf = f.read()
    if tile_pbf.endswith(b"\r\n"):  # weird line feeds when reading on windows
        tile_pbf = tile_pbf[:-2] + b"\n"
    return tile_pbf


@pytest.fixture(scope="class")
def local_server_url(application):
    """Start a listening server and return the base URL."""
    with LocalServer(application) as url:
        yield url


@pytest.fixture(scope="session")
def runner(application):
    """Provide a cli runner for the tests."""
    return application.test_cli_runner()


@pytest.fixture(scope="class")
def webdriver():
    """Provide a selenium/gecko webdriver."""
    try:
        import selenium.webdriver

        options = selenium.webdriver.FirefoxOptions()
        options.add_argument("--headless=new")
        driver = selenium.webdriver.Firefox(options)

        yield driver

        driver.quit()
    except ImportError:
        yield None


@pytest.fixture(scope="session")
def some_online_file_url():
    """Return the URL of a random online file."""
    yield SOME_ONLINE_FILE_URL


@pytest.fixture(scope="session")
def test_data_directory():
    """Return the path to the test data directory."""
    yield TEST_DATA_DIRECTORY


@pytest.fixture(scope="session")
def test_instance_directory():
    """Return the path to the test instance directory."""
    yield TEST_INSTANCE_DIRECTORY
