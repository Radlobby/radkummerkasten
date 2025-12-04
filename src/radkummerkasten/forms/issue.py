#!/usr/bin/env python3


"""A form to upload/save a new issue."""


# from wtforms import (
#     StringField,
#     validators,
# )

from .base import Base
from .field_types import UserId

__all__ = ["Issue"]


class Issue(Base):
    """A form to upload/save a new issue."""

    user_id = UserId("User")
    # issue_type = IssueType("Issue Type")


# TODO, maybe: separate CreateIssue and UpdateIssue?
