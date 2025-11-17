#!/usr/bin/env python3


"""A common sqlalchemy DeclarativeBase to share between models."""


__all__ = ["Base"]


import re
import uuid

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    declared_attr,
    mapped_column,
)

CAMEL_CASE_TO_SNAKE_CASE_RE = re.compile(
    "((?<=[a-z0-9])[A-Z]|(?!^)(?<!_)[A-Z](?=[a-z]))"
)


def snake_case(camel_case):
    """Convert a `CamelCase` string to `snake_case`."""
    return CAMEL_CASE_TO_SNAKE_CASE_RE.sub(r"_\1", camel_case).lower()


class Base(DeclarativeBase, MappedAsDataclass):
    """Template for sqlalchemy declarative_base() to add shared functionality."""

    id: Mapped[uuid.UUID] = mapped_column(
        init=False,
        primary_key=True,
        insert_default=uuid.uuid4,
        default=None,
    )

    @declared_attr.directive
    def __tablename__(cls):
        """Return a table name derived from the class name."""
        return f"{snake_case(cls.__name__)}"

    def __repr__(self):
        """Return a simplified __repr__ to avoid recursion."""
        return f"{self.__class__.__name__}(id={self.id})"
