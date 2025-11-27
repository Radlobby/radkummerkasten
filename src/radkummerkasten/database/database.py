#!/usr/bin/env python3


"""Define a database engine."""


import pathlib

import sqlalchemy

from .models import Base
from .session import Session

__all__ = ["Database"]


PACKAGE = __package__.split(".", maxsplit=1)[0]


class Database:
    """A database engine, handling file and table creation, and pooling."""

    EXTENSION_NAME = f"{PACKAGE}-database"

    def __init__(self, application=None):
        """Start a database engine."""
        self.path = None
        self.engine = None
        if application is not None:
            self.init_app(application)

    def __del__(self):
        """Ensure that all connections are closed when exiting."""
        self.engine.dispose()
        del self.engine

    def init_app(self, application):
        """Initialise a Flask application."""
        if self.EXTENSION_NAME in application.extensions:
            raise RuntimeError(f"A {self.EXTENSION_NAME} extension exists already.")

        application.extensions[self.EXTENSION_NAME] = self

        self.path = (
            pathlib.Path(application.instance_path) / "database" / f"{PACKAGE}.sqlite"
        )
        self.path.parent.mkdir(parents=True, exist_ok=True)

        self._create_database()

    def _create_database(self):
        """Create the database file and tables."""
        self.engine = sqlalchemy.create_engine(f"sqlite:///{self.path}")
        with self.engine.connect():
            Base.metadata.create_all(self.engine)

    @property
    def session(self):
        """Return a session instance."""
        return sqlalchemy.orm.sessionmaker(self.engine, class_=Session)
