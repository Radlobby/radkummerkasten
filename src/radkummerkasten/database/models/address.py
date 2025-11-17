#!/usr/bin/env python3


"""The database model for addresses on the radkummerkasten map."""


from typing import List

from sqlalchemy.orm import (
    Mapped,
    relationship,
)

from .base import Base

__all__ = ["Address"]


class Address(Base):
    """An address (most likely related to an issue reported to radkummerkasten map)."""

    postcode: Mapped[int | None]
    municipality: Mapped[str | None]
    street: Mapped[str | None]
    housenumber: Mapped[str | None]

    issues: Mapped[List["Issue"]] = relationship(  # noqa: F821
        back_populates="address",
        default_factory=list,
    )
