#!/usr/bin/env python


import pytest


@pytest.mark.skipif(not is_selenium_installed)
class Test_Frontend:
    def test_frontend(self, webdriver, live_server_url):
        response = webdriver.get(f"{live_server_url}/")
