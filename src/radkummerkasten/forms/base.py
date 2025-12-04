#!/usr/bin/env python3


"""Forms (using WTForms) that are used in API calls and the frontend."""


import datetime
import os

from wtforms import Form
from wtforms.csrf.session import SessionCSRF

__all__ = ["Base"]


CSRF_SECRET = os.urandom(16)


class Base(Form):
    """Base class for all forms."""

    class Meta:
        """Meta class for the base class."""

        csrf = True
        csrf_class = SessionCSRF
        csrf_secret = CSRF_SECRET
        csrf_time_limit = datetime.timedelta(minutes=30)
