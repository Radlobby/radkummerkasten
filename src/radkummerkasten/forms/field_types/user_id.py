#!/usr/bin/env python3


"""A custom wtforms.Field for user ids."""


import uuid

import wtforms

from ...database import Database
from ...database.models import User


__all__ = [
    "UserId",
]


class UserId(wtforms.Field):
    """A custom wtforms.Field for user ids."""
    widget = wtforms.widgets.HiddenInput()

    def process_formdata(self, valuelist):
        """Format and type-cast form data."""
        if valuelist:
            self.data = uuid.UUID(valuelist[0])

    def post_validate(self, form, validation_stopped):
        """Check whether a user with this user_id exists."""
        if not validation_stopped:
            user_id = self.data
            with Database.session() as session:
                user = session.get(User, user_id)
                if user is None:
                    self.errors.append("User not found")

# TODO: this might be better implemented as custom validators, see
# https://wtforms.readthedocs.io/en/3.2.x/validators/#custom-validators
