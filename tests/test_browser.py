#!/usr/bin/env python


import functools

import pytest


@functools.cache
def is_selenium_installed():
    """Test whether we can use selenium+firefox."""
    try:
        import selenium.webdriver

        options = selenium.webdriver.FirefoxOptions()
        options.add_argument("--headless=new")
        driver = selenium.webdriver.Firefox(options)
        driver.quit()
        selenium_installed = True
    except ImportError:
        selenium_installed = False
    return selenium_installed


@pytest.mark.skipif(
    not is_selenium_installed(), reason="Selenium and/or Firefox not found"
)
class TestFrontend:
    """Test the frontend in a headless browser."""

    def test_frontend(self, webdriver, local_server_url):
        webdriver.get(f"{local_server_url}/")
        assert "Radkummerkasten" in webdriver.title
        webdriver.quit()
