#!/usr/bin/env python3


"""Define a database engine."""


import pathlib

import sqlalchemy

from .models import Base
from .session import Session

__all__ = ["Engine"]


PACKAGE = __package__.split(".", maxsplit=1)[0]


class Engine:
    """A database engine, handling file and table creation, and pooling."""

    def __init__(self, instance_path):
        """Start a database engine."""
        self.path = pathlib.Path(instance_path) / "database" / f"{PACKAGE}.sqlite"
        self.path.parent.mkdir(parents=True, exist_ok=True)

        self._engine = sqlalchemy.create_engine(
            f"sqlite:///{self.path}",
            connect_args={"autocommit": False},
        )
        with self._engine.connect():
            Base.metadata.create_all(self._engine)

    def __del__(self):
        """Ensure that all connections are closed when exiting."""
        self._engine.dispose()
        del self._engine

    @property
    def session(self):
        """Return a session instance."""
        return sqlalchemy.orm.sessionmaker(
            self._engine,
            class_=Session,
            autoflush=False,
        )
