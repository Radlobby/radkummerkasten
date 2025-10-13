#!/usr/bin/env python3


"""Look up the closest street address for a pair of coordinates."""


import os

import geopandas
import pathlib
import shapely


__all__ = [
    "AddressLookup",
]


# Increase cache for faster sindex lookup
os.environ["OGR_SQLITE_CACHE"] = "128"


class AddressLookup:
    """Look up an address."""

    def __init__(self, voronoi_polygons):
        """Look up an address."""
        self.voronoi_polygons = pathlib.Path(voronoi_polygons).resolve()

    def lookup_address(self, lon, lat):
        """Look up an address from a pair of coordinates."""
        point = shapely.Point(lon, lat)
        try:
            record = geopandas.read_file(self.voronoi_polygons, mask=point, rows=1).iloc[0]

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
