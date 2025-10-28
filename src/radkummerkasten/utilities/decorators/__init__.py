#!/usr/bin/env python3


"""Decorators for flask views, blueprints, and methods."""


from .csp_allow_self import csp_allow_self
from .local_referer_only import local_referer_only

# from .login_required import login_required

__all__ = [
    "csp_allow_self",
    "local_referer_only",
    # "login_required",
]
