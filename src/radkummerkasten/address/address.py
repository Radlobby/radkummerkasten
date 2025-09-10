#!/usr/bin/env python3


"""Look up the closest street address for a pair of coordinates."""


import flask
import geopandas
import shapely

from ..utilities import RemotePath
from ..utilities.decorator import local_referer_only

# TODO: move to config
VORONOI_POLYGONS = RemotePath(
    "https://christophfink.github.io"
    "/austrian-addresses"
    "/austrian-addresses-voronoi.gpkg.zip"
)
RANDOM_POINT = shapely.Point(16, 48)


__all__ = [
    "Address",
]


class Address(flask.Blueprint):
    """Provide a blueprint for address lookup."""

    _NAME = "address"
    _IMPORT_NAME = __name__
    _kwargs = {
        "url_prefix": "/address",
    }

    def __init__(self, *args, **kwargs):
        """Provide a blueprint for address lookup."""
        kwargs = kwargs or {}
        kwargs.update(self._kwargs)
        super().__init__(self._NAME, self._IMPORT_NAME, *args, **kwargs)

        self._data = geopandas.read_file(VORONOI_POLYGONS)

        # look up one point to prime spatial index
        _ = self._data.sindex.query(RANDOM_POINT)

        self.add_url_rule(
            "/by-coordinates/<float:lon>,<float:lat>",
            view_func=self.look_up_address,
            methods=("GET",),
        )

    @local_referer_only
    def look_up_address(self, lon, lat):
        """Look up an address from a pair of coordinates."""
        point = shapely.Point(lon, lat)
        try:
            record = self._data[["city", "postcode", "street", "housenumber"]].loc[
                self._data.sindex.query(
                    point,
                    predicate="within",
                )[0]
            ]

            address = {
                "city": record["city"],
                "postcode": record["postcode"],
                "street": record["street"],
                "housenumber": record["housenumber"],
            }
            if address["street"] is None:
                address["street"] = address["city"]
        except IndexError:
            address = {
                "error": "Address not found",
            }
        return address
