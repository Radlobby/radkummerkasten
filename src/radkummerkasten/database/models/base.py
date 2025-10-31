#!/usr/bin/env python3


"""A common sqlalchemy DeclarativeBase to share between models."""


__all__ = ["Base"]


import re

import sqlalchemy.orm

CAMEL_CASE_TO_SNAKE_CASE_RE = re.compile(
    "((?<=[a-z0-9])[A-Z]|(?!^)(?<!_)[A-Z](?=[a-z]))"
)


def snake_case(camel_case):
    """Convert a `CamelCase` string to `snake_case`."""
    return CAMEL_CASE_TO_SNAKE_CASE_RE.sub(r"_\1", camel_case).lower()


class Base(sqlalchemy.orm.DeclarativeBase, sqlalchemy.orm.MappedAsDataclass):
    """Template for sqlalchemy declarative_base() to add shared functionality."""

    @sqlalchemy.orm.declared_attr
    def __tablename__(cls):
        """Return a table name derived from the class name."""
        return f"{snake_case(cls.__name__)}s"
