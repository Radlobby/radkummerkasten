#!/usr/bin/env python3


"""A decorator for flask views and methods that requires login."""


import functools

import flask


def login_required(f):
    """Decorate a flask method to require login."""
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if flask.g.user is None:
            return flask.redirect(flask.url_for("login", next=flask.request.url))
        return f(*args, **kwargs)

    return decorated_function
