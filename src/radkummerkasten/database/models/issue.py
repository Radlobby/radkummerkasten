#!/usr/bin/env python3


"""The database model for issues on the radkummerkasten map."""


import datetime
import uuid

from sqlalchemy import (
    ForeignKey,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from .base import Base
from .issue_type import IssueType

__all__ = ["Issue"]


class Issue(Base):
    """
    An issue reported to radkummerkasten map.

    Note that the first comment to this issue is shown as the issue text.
    """

    issue_type: Mapped[IssueType]

    datetime: Mapped[datetime.datetime]

    lon: Mapped[float]
    lat: Mapped[float]

    likes: Mapped[int] = mapped_column(default=0)

    address_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("address.id"),
        init=False,
    )
    address: Mapped["Address"] = relationship(  # noqa: F821
        back_populates="issues",
        default=None,
    )
