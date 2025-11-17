#!/usr/bin/env python3


"""The database model for media attached to comments on the radkummerkasten map."""


import pathlib
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

__all__ = ["Media"]


class Media(Base):
    """
    Some media attached to a comment on the radkummerkasten map.

    Currently restricted to photos/images.
    """

    comment_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("comment.id"), init=False,)
    comment: Mapped["Comment"] = relationship(back_populates="media", default=None,)  # noqa: F821

    @property
    def file_path(self):
        """Return a “computed column”, that derives a file path from the id."""
        self_id = str(self.id)
        return pathlib.Path(f"{self_id[:1]}/{self_id[:2]}/{self_id}.webp")
