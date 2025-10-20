#!/usr/bin/env python3


"""Define a database engine."""


import pathlib

import geoalchemy2
import sqlalchemy

__all__ = ["DatabaseEngine"]


PACKAGE = __package__.split(".", maxsplit=1)[0]


class DatabaseEngine:
    """A database engine, handling file and table creation, and pooling."""

    def __init__(self, instance_path):
        """Start a database engine."""
        self.path = pathlib.Path(instance_path) / "database" / f"{PACKAGE}.gpkg"
        self.path.parent.mkdir(parents=True, exist_ok=True)

        self._engine = sqlalchemy.create_engine(f"gpkg://{self.path}")
        sqlalchemy.event.listen(
            self._engine,
            "connect",
            geoalchemy2.load_spatialite_gpkg,
        )

    def __enter__(self):
        """Use this engine."""
        return self._engine

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit database engine context."""
