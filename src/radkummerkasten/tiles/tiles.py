#!/usr/bin/env python3


"""Serve vector tiles."""


import functools

import flask

from ..core import tiles
from ..utilities.decorators import local_referer_only

__all__ = [
    "Tiles",
]


class Tiles(flask.Blueprint):
    """Serve vector tiles."""

    _NAME = "tiles"
    _IMPORT_NAME = __name__
    _kwargs = {
        "url_prefix": "/",
    }

    def __init__(self, tile_layers, *args, **kwargs):
        """Provide a blueprint for vector tiles."""
        kwargs = kwargs or {}
        kwargs.update(self._kwargs)
        super().__init__(self._NAME, self._IMPORT_NAME, *args, **kwargs)

        self._tiles = {}
        for tile_layer in tile_layers:
            self._tiles[tile_layer] = tiles.Tiles(tile_layer)
            self.add_url_rule(
                "/<string:tile_layer>/<int:z>/<int:x>/<int:y>",
                view_func=self.tile,
                methods=("GET",),
            )

    # TODO: implement etag matching
    @local_referer_only
    def tile(self, z, x, y, tile_layer):
        """Serve a vector tile."""
        try:
            tile = self._tiles[tile_layer].tile(z, x, y)
            assert tile is not None
        except (
            AssertionError,  # tile not found
            KeyError,  # layer not found
        ):
            response = (
                flask.jsonify(
                    error=f"Tile {z}/{x}/{y} of layer {tile_layer} not found."
                ),
                404,
            )
        else:
            response = flask.Response(tile, mimetype="application/x-protobuf")
        return response
