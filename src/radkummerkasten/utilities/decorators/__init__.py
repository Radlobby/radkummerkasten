#!/usr/bin/env python3


"""Decorators for flask views, blueprints, and methods."""


from .local_referer_only import local_referer_only

# from .login_required import login_required

__all__ = [
    "local_referer_only",
    # "login_required",
]
