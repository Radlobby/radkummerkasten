#!/usr/bin/env python3


"""Define a database engine."""


import pathlib

import sqlalchemy

__all__ = ["DatabaseEngine"]


PACKAGE = __package__.split(".", maxsplit=1)[0]


class DatabaseEngine:
    """A database engine, handling file and table creation, and pooling."""

    def __init__(self, instance_path):
        """Start a database engine."""
        self.path = pathlib.Path(instance_path) / "database" / f"{PACKAGE}.sqlite"
        self.path.parent.mkdir(parents=True, exist_ok=True)

        self._engine = sqlalchemy.create_engine(
            f"sqlite:///{self.path}",
            connect_args={"autocommit": False},
        )
        self._engine.connect()  # create database

    def __enter__(self):
        """Use this engine."""
        return self._engine

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit database engine context."""

    @property
    def session(self):
        """Return a session instance."""
        return sqlalchemy.orm.sessionmaker(self._engine, autoflush=False)()
