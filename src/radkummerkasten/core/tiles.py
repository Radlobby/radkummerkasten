#!/usr/bin/env python3


"""Compute vector tiles of a dataset for a given zoom level and tile index."""

import io
import json
import pathlib

import flask
import geopandas
from geojson2vt import geojson2vt
from vt2pbf import vt2pbf

__all__ = [
    "Tiles",
]


EMPTY_TILE = vt2pbf({"features": []})


class Tiles:
    """Compute vector tiles of a dataset for a zoom level and tile index."""

    def __init__(self, data, layer_name):
        """
        Compute vector tiles of one of more datasets.

        Arguments
        ---------
        data : geopandas.GeoDataFrame | pathlib.Path
            the layer to serve
        layer_name : str
            the name of this layer (included, e.g., in the tilejson metadata)
        """
        self.bounds = None
        self.layer_name = layer_name
        self.tile_index = None
        self.reload_data(data)

    @staticmethod
    def _geodataframe_to_geojson(gdf):
        # The default implementation of geopandas.GeoDataFrame.to_json()
        # always casts "id" to str, which is (a) weird and (b) not accepted by
        # geojson2vt (weird, too).
        #
        # https://github.com/geopandas/geopandas/blob/
        # 4f9f361a2ba94db4c02e1fb5b6b2b09abf4278e6/geopandas/geodataframe.py#L1166
        buffer = io.BytesIO()
        gdf.to_file(buffer, driver="GeoJSON")
        buffer.seek(0)
        return json.load(buffer)

    def tile(self, z, x, y):
        """
        Retrieve the vector tile at tile index `x`, `y` for zoom level `z`.

        Arguments
        ---------
        x, y, z : int
            coordinates and zoom level of the tile requested
        """
        tile = self.tile_index.get_tile(z, x, y)
        if tile is None:
            tile = EMPTY_TILE
        else:
            tile = vt2pbf(tile)
        return tile

    @property
    def tilejson(self):
        """Return metadata for this tile layer."""
        # https://github.com/mapbox/tilejson-spec/tree/master/3.0.0
        tilejson = {
            "tilejson": "3.0.0",
            "name": self.layer_name,
            "description": self.layer_name,
            "tiles": [self.tile_url],
            "bounds": self.bounds,
            "vector_layers": [
                {
                    "id": self.layer_name,
                    "fields": {field: field for field in self.fields},
                }
            ],
        }
        return tilejson

    @property
    def tile_url(self):
        """Return the URL template for fetching tiles."""
        tile_layer_url = flask.url_for(
            "tiles.tilejson",
            tile_layer=self.layer_name,
            _external=True,
        )
        return f"{tile_layer_url}" "/{z}/{x}/{y}"

    def reload_data(self, data):
        """
        Reload the underlying data.

        Arguments
        ---------
        data : geopandas.GeoDataFrame | pathlib.Path
            reload the data from this GeoDataFrame/file readable by
            ``geopandas.read_file()``
        """
        if isinstance(data, pathlib.Path):
            data = geopandas.read_file(data)
        else:
            data = geopandas.GeoDataFrame(data)

        data = data.to_crs("EPSG:4326")

        bounds = [float(coordinate) for coordinate in data.total_bounds]
        fields = [str(column_name) for column_name in data.columns]
        data = self._geodataframe_to_geojson(data)

        self.tile_index = geojson2vt.GeoJsonVt(
            data,
            options={"maxZoom": 24},
        )
        self.bounds = bounds
        self.fields = fields
