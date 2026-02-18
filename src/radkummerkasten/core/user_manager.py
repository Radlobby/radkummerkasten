#!/usr/bin/env python3


"""Interact with user profiles."""


import datetime
# import hashlib
# import hmac
# import secrets

import flask

from ..database import Database
from ..database.models import (
    User,
)

__all__ = ["UserManager"]


class UserManager:
    """Interact with user profiles."""

    @property
    def database(self):
        """Retrieve a radkummerkasten.database.Database instance."""
        database = flask.current_app.extensions[Database.EXTENSION_NAME]
        return database

    @property
    def current_user(self):
        """Fetch the currently logged-in user’s details."""
        with self.database.session() as session:
            user_id = flask.session.get("user")
            user = session.get(User, user_id)
            if user is not None:
                session.expunge(user)
        return user
