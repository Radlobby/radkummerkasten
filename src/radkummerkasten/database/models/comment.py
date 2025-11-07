#!/usr/bin/env python3


"""The database model for comments on the radkummerkasten map."""


import uuid
from typing import List

from sqlalchemy import (
    ForeignKey,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from .base import Base

__all__ = ["Comment"]


class Comment(Base):
    """
    A comment attached to an issue reported to radkummerkasten map.

    Note that the first comment to an issue is shown as the issue text.
    """

    text: Mapped[str]
    media: Mapped[List["Media"]] = relationship(back_populates="comment")  # noqa: F821

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="comments")  # noqa: F821
