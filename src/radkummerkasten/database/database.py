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
        if application is not None:
            self.init_app(application)

        self.path = None
        self.engine = None

    def init_app(self, application):
        """Initialise a Flask application."""
        if self.EXTENSION_NAME in application.extensions:
            raise RuntimeError(f"A {self.EXTENSION_NAME} extension exists already.")

        application.extensions[self.EXTENSION_NAME] = self
        # application.teardown_appcontext(self._teardown_session)

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

    # def _teardown_session(self):
    #     """Handle application teardown"""
    #     self.engine.dispose()
    #     del self.engine

    @property
    def session(self):
        """Return a session instance."""
        return sqlalchemy.orm.sessionmaker(self.engine, class_=Session)


# @sqlalchemy.event.listens_for(Session, "after_commit")
# def update_geopackage_if_changed(session):
#     """Update the geopackage copy of the issue table."""
#
#     # Do not run outside application context
#     try:
#         _ = flask.current_app.instance_path
#     except RuntimeError:
#         return
#
#     with Database().session.begin() as session:
#         data = {
#             "id": [],
#             "lon": [],
#             "lat": [],
#         }
#         for issue_id, lon, lat in session.execute(
#             sqlalchemy.select(Issue.id, Issue.lon, Issue.lat)
#         ):
#             data["id"].append(issue_id)
#             data["lon"].append(lon)
#             data["lat"].append(lat)
#
#         issues = geopandas.GeoDataFrame(
#             {
#                 "id": data["id"],
#                 "geometry": geopandas.points_from_xy(
#                     data["lon"],
#                     data["lat"],
#                     crs="EPSG:4326",
#                 ),
#             }
#         )
#         issues.to_file(
#             pathlib.Path(flask.current_app.instance_path)
#             / "database"
#             / f"{PACKAGE}.gpkg"
#         )
