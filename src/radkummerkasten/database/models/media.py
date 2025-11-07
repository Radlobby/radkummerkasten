#!/usr/bin/env python3


"""The database model for media attached to comments on the radkummerkasten map."""


import os
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

    file_path: Mapped[os.PathLike] = mapped_column()

    comment_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("comment.id"))
    comment: Mapped["Comment"] = relationship(back_populates="media")  # noqa: F821
