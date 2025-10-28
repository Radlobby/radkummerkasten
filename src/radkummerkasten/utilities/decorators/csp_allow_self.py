#!/usr/bin/env python3


"""A decorator to add a Content-Security-Policy header."""


import flask_cors

__all__ = ["csp_allow_self"]


def csp_allow_self(f):
    """Decorate a view to add a Content-Security-Policy header."""
    return flask_cors.cross_origin("default-src: 'self';")(f)
