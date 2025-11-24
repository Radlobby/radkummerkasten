#!/usr/bin/env python3


"""The database model for addresses on the radkummerkasten map."""


from sqlalchemy.orm import (
    Mapped,
)

from .base import Base

__all__ = ["Address"]


class Address(Base):
    """An address (related to an issue reported to radkummerkasten map)."""

    street: Mapped[str | None]
    housenumber: Mapped[str | None]
    postcode: Mapped[int | None]
    municipality: Mapped[str | None]
