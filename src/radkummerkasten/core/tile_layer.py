#!/usr/bin/env python3


"""Compute vector tiles of a dataset for a given zoom level and tile index."""


import functools

import flask
import geopandas
import mercantile
import shapely
import vt2pbf

from ..utilities import BytesCache

__all__ = [
    "TileLayer",
]


MAX_ZOOM = 24
TILE_WIDTH = TILE_HEIGHT = 4096
TILE_BUFFER = 64


class TileLayer:
    """Compute vector tiles of a dataset for a zoom level and tile index."""

    EMPTY_TILE = vt2pbf.Tile().serialize_to_bytestring()

    def __init__(self, data, layer_name):
        """
        Compute vector tiles of one of more datasets.

        Arguments
        ---------
        data : pathlib.Path
            the layer to serve, in a format readable by geopandas.read_file,
            preferrably containing a spatial index
        layer_name : str
            the name of this layer (included, e.g., in the tilejson metadata)
        """
        self.bounds = None
        self.data = data
        self.layer_name = layer_name
        self.cache = BytesCache(layer_name)

        try:
            data = geopandas.read_file(self.data)
            self.bounds = [float(coordinate) for coordinate in data.total_bounds]
            self.fields = [str(column_name) for column_name in data.columns]
            del data
        except Exception as exception:
            raise RuntimeError(f"Could not open tile layer {self.data}.") from exception

    def empty_cache(self):
        """Delete the entire content of the cache."""
        self.cache.empty()

    def expire_cache_for_lon_lat(self, lon, lat):
        """
        Delete the cached tile that covers/contains a point.

        Arguments
        ---------
        lon : float
        lat : float
            coordinates of a point
        """
        tile = mercantile.tile(lon, lat, MAX_ZOOM)
        while tile is not None:
            self.cache.expire(f"{tile.z}/{tile.x}/{tile.y}", now=True)
            tile = mercantile.parent(tile)

    def tile(self, z, x, y):
        """
        Retrieve the vector tile at tile index `x`, `y` for zoom level `z`.

        Arguments
        ---------
        x, y, z : int
            coordinates and zoom level of the tile requested
        """
        try:
            tile = self.cache[f"{z}/{x}/{y}"]
        except KeyError:
            bounds = mercantile.bounds(mercantile.Tile(x, y, z))
            left, bottom, right, top = bounds
            width = right - left
            height = top - bottom

            # Add a buffer that would be 64 units (of 4096 width) in the output pbf
            mask = shapely.box(*bounds).buffer(width / (TILE_HEIGHT / TILE_BUFFER))

            features = geopandas.read_file(self.data, mask=mask).clip(mask, sort=True)

            if len(features) > 0:
                # make sure we don’t have multigeometries
                features = features.explode()

                # transform to tile coordinate space
                transform_to_tile_coordinate_space = functools.partial(
                    self._transform_to_tile_coordinate_space,
                    origin=(left, bottom),
                    ratio=((TILE_WIDTH / width), (TILE_HEIGHT / height)),
                )
                features["geometry"] = shapely.transform(
                    features["geometry"].force_2d(),
                    transform_to_tile_coordinate_space,
                )

                features = features.reset_index(drop=True)
                features["id"] = features.index

                features = features.apply(self._convert_feature, axis=1).to_list()

                tile = vt2pbf.service.tile.Tile()
                tile.add_layer(self.layer_name, features)
                tile = tile.serialize_to_bytestring()

            else:
                tile = self.EMPTY_TILE

            self.cache[f"{z}/{x}/{y}"] = tile

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

    @staticmethod
    def _transform_to_tile_coordinate_space(
        coordinates,
        origin,
        ratio,
    ):
        coordinates = coordinates.swapaxes(0, 1)
        coordinates[0] = (coordinates[0] - origin[0]) * ratio[0]
        coordinates[1] = TILE_HEIGHT - ((coordinates[1] - origin[1]) * ratio[1])
        coordinates = coordinates.swapaxes(0, 1)
        return coordinates

    @staticmethod
    def _convert_feature(row):
        row = row.to_dict()
        id_ = row.pop("id")
        geometry = row.pop("geometry")

        geometry_type = 0  # UNKNOWN
        coordinates = []
        if geometry.geom_type == "Point":
            geometry_type = 1
            coordinates = [
                [round(geometry.x), round(geometry.y)],
            ]
        elif geometry.geom_type == "LineString":
            geometry_type = 2
            coordinates = [
                [[round(x), round(y)] for x, y in geometry.coords],
            ]
        elif geometry.geom_type == "Polygon":
            coordinates = [
                [
                    [[round(x), round(y)] for x, y in part.coords]
                    for part in [geometry.exterior] + list(geometry.interiors)
                ],
            ]
            geometry_type = 3

        feature = {
            "id": id_,
            "geometry": coordinates,
            "tags": row,
            "type": geometry_type,
        }

        return feature
