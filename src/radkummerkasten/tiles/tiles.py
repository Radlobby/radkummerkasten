#!/usr/bin/env python3


"""Serve vector tiles."""


import flask

from ..core import tiles
from ..utilities.decorators import local_referer_only

__all__ = [
    "Tiles",
]


class Tiles(flask.Blueprint):
    """Serve vector tiles."""

    _NAME = "address"
    _IMPORT_NAME = __name__
    _kwargs = {
        "url_prefix": "/",
    }

    def __init__(self, *args, **kwargs):
        """Provide a blueprint for vector tiles."""
        kwargs = kwargs or {}
        kwargs.update(self._kwargs)
        super().__init__(self._NAME, self._IMPORT_NAME, *args, **kwargs)

        self._tiles = tiles.Tiles()
        self.add_url_rule(
            "/<int:z>/<int:x>/<int:y>",
            view_func=self.tile,
            methods=("GET",),
        )

    # TODO: implement etag matching
    @local_referer_only
    def tile(self, z, x, y):
        """Serve a vector tile."""
        tile = self._tiles.tile(z, x, y)
        if tile is None:
            return flask.jsonify(error=f"Tile {z}/{x}/{y} not found."), 404
        else:
            return flask.Response(tile, mimetype="application/x-protobuf")
