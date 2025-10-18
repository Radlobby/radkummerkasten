#!/usr/bin/env python3


"""Serve vector tiles."""


import flask

from ..core import TileLayer
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

    def __init__(self, configuration, *args, **kwargs):
        """Provide a blueprint for vector tiles."""
        kwargs = kwargs or {}
        kwargs.update(self._kwargs)
        super().__init__(self._NAME, self._IMPORT_NAME, *args, **kwargs)

        try:
            tile_layers = configuration["TILE_LAYERS"]
        except KeyError:
            tile_layers = {}

        self.tile_layers = {}
        for tile_layer_name, tile_layer_source in tile_layers.items():
            self.tile_layers[tile_layer_name] = TileLayer(
                tile_layer_source, tile_layer_name
            )
            self.add_url_rule(
                "/<string:tile_layer>/<int:z>/<int:x>/<int:y>",
                view_func=self.tile,
                methods=("GET",),
            )
            self.add_url_rule(
                "/<string:tile_layer>",
                view_func=self.tilejson,
                methods=("GET",),
            )

    # TODO: implement etag matching
    @local_referer_only
    def tile(self, z, x, y, tile_layer):
        """Serve a vector tile."""
        try:
            tile = self.tile_layers[tile_layer].tile(z, x, y)
        except KeyError:
            response = (
                flask.jsonify(error=f"Tile layer {tile_layer} not found."),
                404,
            )
        else:
            response = flask.Response(tile, mimetype="application/x-protobuf")
        return response

    # TODO: implement etag matching
    @local_referer_only
    def tilejson(self, tile_layer):
        """Serve the metadata about a tile layer."""
        try:
            tilejson = self.tile_layers[tile_layer].tilejson
        except KeyError:
            response = (
                flask.jsonify(error=f"Tile layer {tile_layer} not found."),
                404,
            )
        else:
            response = flask.jsonify(tilejson)
        return response
