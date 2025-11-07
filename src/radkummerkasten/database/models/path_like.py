#!/usr/bin/env python3


"""Allow mapping an os.Pathike object to an sqlalchemy.String."""


import os
import typing

import sqlalchemy
import sqlalchemy.types

__all__ = ["PathLike"]


class PathLike(sqlalchemy.types.TypeDecorator):
    """Allow mapping an os.Pathike object to an sqlalchemy.String."""

    impl = sqlalchemy.String

    def __init__(self, factory: typing.Callable[[str], os.PathLike]):
        """Allow mapping an os.Pathike object to an sqlalchemy.String."""
        super().__init__()
        self.factory = factory

    def process_bind_param(
        self,
        value: typing.Optional[os.PathLike],
        dialect: sqlalchemy.Dialect,
    ) -> str:
        """Convert an os.PathLike value to a string for the database."""
        if value:
            value = os.fspath(value)
        return value

    def process_result_value(
        self,
        value: typing.Optional[str],
        dialect: sqlalchemy.Dialect,
    ) -> typing.Optional[os.PathLike]:
        """Restore a string from the database to an os.Pathlike."""
        if value is not None:
            value = self.factory(value)
        return value
