#!/usr/bin/env python3


"""Common fixtures and settings for testing radkummerkasten."""

import os
import pathlib
import tempfile

import pytest

import radkummerkasten

from .local_server import LocalServer

DATA_DIRECTORY = (pathlib.Path(__file__).parent / "data").absolute()
INSTANCE_DIRECTORY = (pathlib.Path(__file__).parent / "instance").absolute()

TILE_LAYER_FILE = INSTANCE_DIRECTORY / "data" / "radlkarte-wien.geojson"


@pytest.fixture(scope="session")
def application(instance_directory):
    """Start a flask application."""
    os.environ["TESTING"] = "TRUE"
    application = radkummerkasten.create_app(instance_path=instance_directory)
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


@pytest.fixture(scope="session")
def data_directory():
    """Return the path to the test data directory."""
    yield DATA_DIRECTORY


@pytest.fixture(scope="function")
def expected_tile_json(request, data_directory):
    """Read the expected content of a vector tile from disk."""
    return pathlib.Path(data_directory / f"{request.param}.tilejson").read_text()


@pytest.fixture(scope="function")
def expected_tile_pbf(request, data_directory):
    """Read the expected content of a vector tile from disk."""
    with (data_directory / f"{request.param}.pbf").open("rb") as f:
        tile_pbf = f.read()
    if tile_pbf.endswith(b"\r\n"):  # weird line feeds when reading on windows
        tile_pbf = tile_pbf[:-2] + b"\n"
    return tile_pbf


@pytest.fixture(scope="session")
def instance_directory():
    """Return the path to the test instance directory."""
    yield INSTANCE_DIRECTORY


@pytest.fixture(scope="class")
def local_server_url(application):
    """Start a listening server and return the base URL."""
    with LocalServer(application) as url:
        yield url


@pytest.fixture(scope="session")
def runner(application):
    """Provide a cli runner for the tests."""
    return application.test_cli_runner()


@pytest.fixture(scope="session")
def tile_layer_file():
    """Return the path to a test tile layer file."""
    yield TILE_LAYER_FILE


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
