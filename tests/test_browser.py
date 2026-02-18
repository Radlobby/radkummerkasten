#!/usr/bin/env python


"""Browser testing."""

import functools

import pytest
import pytest_lazy_fixtures


@functools.cache
def is_selenium_installed():
    """Test whether we can use selenium+firefox."""
    webdriver = pytest_lazy_fixtures.lf("webdriver")
    return webdriver is not None


@pytest.mark.skipif(
    not is_selenium_installed(),
    reason="Selenium and/or Firefox not found",
)
class TestFrontend:
    """Test the frontend in a headless browser."""

    def test_frontend(self, webdriver, local_server_url):
        """Test the frontend in a headless browser."""
        webdriver.get(f"{local_server_url}/")
        assert "Radkummerkasten" in webdriver.title
        webdriver.quit()
