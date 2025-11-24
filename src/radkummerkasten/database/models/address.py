#!/usr/bin/env python3


"""The database model for addresses on the radkummerkasten map."""


from typing import Optional

from sqlalchemy.orm import (
    Mapped,
)

from .base import Base

__all__ = ["Address"]


class Address(Base):
    """An address (related to an issue reported to radkummerkasten map)."""

    street: Mapped[Optional[str]]
    housenumber: Mapped[Optional[str]]
    postcode: Mapped[Optional[int]]
    municipality: Mapped[Optional[str]]
