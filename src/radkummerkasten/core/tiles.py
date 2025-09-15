#!/usr/bin/env python3


"""Compute vector tiles of a dataset for a given zoom level and tile index."""

import json

from geojson2vt import geojson2vt
from vt2pbf import vt2pbf

from ..utilities import RemotePath

# TODO: move to config
# TODO: relate to our data, on the fly
RADLKARTE_GEOJSON = RemotePath(
    "https://raw.githubusercontent.com/"
    "markusstraub/radlkarte/"
    "refs/heads/main/"
    "data/radlkarte-wien.geojson"
)


__all__ = [
    "Tiles",
]


class Tiles:
    """Compute vector tiles of a dataset for a given zoom level and tile index."""

    def __init__(self, *args, **kwargs):
        """Compute vector tiles of a dataset for a given zoom level and tile index."""
        with RADLKARTE_GEOJSON.open() as f:
            data = json.load(f)
        self._tile_index = geojson2vt.GeoJsonVt(
            # json.loads(geopandas.read_file(RADLKARTE_GEOJSON).to_json()),  #
            # feature_id is str, that’s a problem
            data,
            {"maxZoom": 24},
        )

    def tile(self, z, x, y):
        """Retrieve the vector tile at tile index `x`, `y` for zoom level `z`."""
        tile = self._tile_index.get_tile(z, x, y)
        if tile is not None:
            tile = vt2pbf(tile)
        return tile
