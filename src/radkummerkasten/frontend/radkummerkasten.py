#!/usr/bin/env python3


"""Return the single-page radkummerkasten front page."""


import flask

__all__ = [
    "Radkummerkasten",
]


class Radkummerkasten(flask.Blueprint):
    """Provide a blueprint for radkummerkasten front page."""

    _NAME = "radkummerkasten"
    _IMPORT_NAME = __name__
    _kwargs = {
        "url_prefix": "/",
        "template_folder": "templates",
    }

    def __init__(self, *args, **kwargs):
        """Provide a blueprint for radkummerkasten lookup."""
        kwargs = kwargs or {}
        kwargs.update(self._kwargs)
        super().__init__(self._NAME, self._IMPORT_NAME, *args, **kwargs)

        self.add_url_rule(
            "/",
            view_func=self.radkummerkasten,
            methods=("GET",),
        )

    def radkummerkasten(self):
        """Return the single-page radkummerkasten front page."""
        return flask.render_template("index.html")
