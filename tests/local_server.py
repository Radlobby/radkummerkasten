#!/usr/bin/python3


"""A locally listening flask server for testing."""

import contextlib
import functools
import socket
import threading

import werkzeug.serving

__all__ = ["LocalServer"]


class _LocalServer(threading.Thread):
    """A locally listening local flask server for testing."""

    def __init__(
        self,
        application,
        host,
        port,
    ):
        """
        Initialise a local flask server of application.

        Arguments
        ---------
        application : flask.Flask
            application to start
        """
        super().__init__()
        self.application = application
        self.host = host
        self.port = port

    def run(self):
        """Start a WSGI server."""
        self.server = werkzeug.serving.BaseWSGIServer(
            self.host, self.port, self.application
        )
        self.server.serve_forever()

    def join(self, timeout=None):
        """Stop the WSGI server and join the thread."""
        self.server.shutdown()
        super().join(timeout)


class LocalServer(threading.Thread):
    """A locally listening local flask server for testing."""

    host = "localhost"

    def __init__(self, application):
        """
        Initialise a local flask server of application.

        Arguments
        ---------
        application : flask.Flask
            application to start
        """
        super().__init__()
        self.server = _LocalServer(application, self.host, self.port)

    def __enter__(self):
        """Provide a context manager for LocalServer."""
        self.server.start()
        return self.url

    def __exit__(self, exc_type, exc_value, traceback):
        """Close a context manager."""
        self.server.join()

    @functools.cached_property
    def port(self):
        """Find an available port."""
        # https://stackoverflow.com/a/45690594
        with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            s.bind((self.host, 0))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            return s.getsockname()[1]

    def __repr__(self):
        """Return a represention of this instance."""
        return f"{self.__class__.__name__}<{self.url}>"

    @property
    def url(self):
        """Return the URL we are listening on."""
        return f"http://{self.host}:{self.port}/"
