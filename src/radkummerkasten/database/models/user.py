#!/usr/bin/env python3


"""The database model for users on the radkummerkasten map."""


import datetime

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from .base import Base

__all__ = ["User"]


class User(Base):
    """A user registered to post to the radkummerkasten map."""

    first_name: Mapped[str]
    last_name: Mapped[str]
    email_address: Mapped[str] = mapped_column(unique=True)

    # comments: Mapped[List["Comment"]] = relationship(  # noqa: F821
    #    back_populates="user",
    #    default_factory=list,
    # )

    can_post: Mapped[bool] = mapped_column(default=False)
    details_confirmed: Mapped[datetime.datetime] = mapped_column(
        default=None, nullable=True
    )
