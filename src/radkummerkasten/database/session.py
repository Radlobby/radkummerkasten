#!/usr/bin/env python3


"""Add custom functions to an sqlalchemy.orm.session.Session."""

import sqlalchemy

__all__ = ["Session"]


PACKAGE = __package__.split(".", maxsplit=1)[0]


class Session(sqlalchemy.orm.Session):
    """An SQLAlchemy session with added functions."""

    def find(self, model, **values):
        """
        Retrieve a database item.

        This searches the database for any item of model that has the values
        defined in **values, returns the first found item, or None

        Arguments
        ---------
        model : any
            sqlalchemy database model to search for (e.g.,
            radkummerkasten.database.models.Issue)
        **values : any
            which values to try to match

        Returns
        -------
        model | None: A fetched or newly created item of type model
        """
        # keep values that are relationships and do not have a primary key
        # defined (-> new!), aside. Add them after finding item
        empty_relationships = {
            key: value
            for key, value in values.items()
            if (
                isinstance(
                    getattr(model, key).property,
                    sqlalchemy.orm.Relationship,
                )
                and (
                    value is None
                    or value == []
                    or value.id is None  # works for us, as pk always "id"
                )
            )
        }
        where_clauses = [
            getattr(model, key) == value
            for key, value in values.items()
            if key not in empty_relationships.keys()
        ]
        try:
            item = self.execute(
                sqlalchemy.select(model).where(*where_clauses)
            ).scalar_one()
        except sqlalchemy.exc.NoResultFound:
            item = None
        return item
