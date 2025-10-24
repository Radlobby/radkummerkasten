#!/usr/bin/env python3


"""Compute vector tiles of a dataset for a given zoom level and tile index."""


import functools

import flask
import geopandas
import mercantile
import shapely
import vt2pbf

__all__ = [
    "TileLayer",
]


MAX_ZOOM = 24
TILE_WIDTH = TILE_HEIGHT = 4096
TILE_BUFFER = 64


class TileLayer:
    """Compute vector tiles of a dataset for a zoom level and tile index."""

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

        self.EMPTY_TILE = vt2pbf.Tile().serialize_to_bytestring()

        try:
            data = geopandas.read_file(self.data)
            self.bounds = [float(coordinate) for coordinate in data.total_bounds]
            self.fields = [str(column_name) for column_name in data.columns]
            del data
        except Exception as exception:
            raise RuntimeError(f"Could not open tile layer {self.data}.") from exception

    def tile(self, z, x, y):
        """
        Retrieve the vector tile at tile index `x`, `y` for zoom level `z`.

        Arguments
        ---------
        x, y, z : int
            coordinates and zoom level of the tile requested
        """
        # TODO: implement caching

        bounds = mercantile.bounds(mercantile.Tile(x, y, z))
        left, bottom, *_ = bounds
        width = bounds[2] - bounds[0]
        height = bounds[3] - bounds[1]

        # Add a buffer that would be 64 units (of 4096 width) in the output pbf
        mask = shapely.box(*bounds).buffer(width / (TILE_HEIGHT / TILE_BUFFER))

        features = geopandas.read_file(self.data, mask=mask).clip(mask)

        if len(features) > 0:
            # make sure we don’t have multigeometries
            features = features.explode()

            # transform to tile coordinate space
            transform_to_tile_coordinate_space = functools.partial(
                self._transform_to_tile_coordinate_space,
                origin_x=left,
                origin_y=bottom,
                ratio_x=(TILE_WIDTH / width),
                ratio_y=(TILE_HEIGHT / height),
            )
            features["geometry"] = shapely.transform(
                features["geometry"].force_2d(),
                transform_to_tile_coordinate_space,
                interleaved=False,
            )

            features = features.reset_index(drop=True)
            features["id"] = features.index

            features = features.apply(self._convert_feature, axis=1).to_list()

            tile = vt2pbf.service.tile.Tile()
            tile.add_layer(self.layer_name, features)
            tile = tile.serialize_to_bytestring()

        else:
            tile = self.EMPTY_TILE
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
        x,
        y,
        origin_x=None,
        origin_y=None,
        ratio_x=None,
        ratio_y=None,
    ):
        x = (x - origin_x) * ratio_x
        y = TILE_HEIGHT - ((y - origin_y) * ratio_y)
        return x, y

    @staticmethod
    def _convert_feature(row):
        row = row.to_dict()
        id_ = row.pop("id")
        geometry = row.pop("geometry")
        coordinates = list(geometry.coords)

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
                    [[round(x), round(y)] for x, y in part]
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
