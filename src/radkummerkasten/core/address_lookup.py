#!/usr/bin/env python3


"""Look up the closest street address for a pair of coordinates."""


import geopandas
import shapely

from ..utilities import RemotePath

# TODO: move to config
VORONOI_POLYGONS = RemotePath(
    "https://christophfink.github.io"
    "/austrian-addresses"
    "/austrian-addresses-voronoi.gpkg.zip"
)
RANDOM_POINT = shapely.Point(16, 48)


__all__ = [
    "AddressLookup",
]


class AddressLookup:
    """Look up an address."""

    def __init__(self, *args, **kwargs):
        """Look up an address."""
        self._data = geopandas.read_file(VORONOI_POLYGONS)

        # look up one point to prime spatial index
        _ = self._data.sindex.query(RANDOM_POINT)

    def lookup_address(self, lon, lat):
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
