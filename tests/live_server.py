#!/usr/bin/python3


"""A locally listening live flask server for testing."""


import time

import requests
import werkzeug.serving

__all__ = ["LiveServer"]


class LiveServer(werkzeug.serving.BaseWSGIServer):
    """A locally listening live flask server for testing."""

    _MAX_RETRIES = 10
    _WAIT_TIME_SEC = 0.5

    def __init__(self, application, host="127.0.0.1", port=5000):
        """
        Initialise a live flask server of application.

        Arguments
        ---------
        application : flask.Flask
            application to start
        """
        super().__init__(host, port, application)
        self.url = f"http://{host}:{port}/"

    def __enter__(self):
        """Provide a context manager for LiveServer."""
        self.serve_forever()

        retries = 0
        while True:
            with requests.get(self.url) as response:
                try:
                    print(response)
                    print(response.status_code)
                    print(self.url)
                    assert response.status_code == 200
                    break
                except AssertionError:
                    retries += 1
                    if retries > self._MAX_RETRIES:
                        raise RuntimeError(f"Could not start {self}")
                    time.sleep(self._WAIT_TIME_SEC)

        return self.url

    def __exit__(self, exc_type, exc_value, traceback):
        """Close a context manager."""
        self.shutdown()

    def __repr__(self):
        """Return a represention of this instance."""
        return f"{self.__class__.__name__}<{self.url}>"
