#!/usr/bin/env python3


"""A form to upload/save a new issue."""


from wtforms import (
    StringField,
    validators,
)

from .base import Base
from .fields import UserId


__all__ = ["Issue"]


class Issue(Base):
    user_id = UserId("User")
    # issue_type = IssueType("Issue Type")

# TODO, maybe: separate CreateIssue and UpdateIssue?
