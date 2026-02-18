#!/usr/bin/env python3


"""A decorator for flask views and methods that allows local referers only."""

import functools

import flask


def local_referer_only(f):
    """Decorate a flask method to allow only local referers."""

    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        # TODO
        # do some magic with flask.request.referrer
        # else: flask.abort(401)
        flask.current_app.logger.info(f"Referer: {flask.request.referrer}")
        return f(*args, **kwargs)

    return decorated_function
