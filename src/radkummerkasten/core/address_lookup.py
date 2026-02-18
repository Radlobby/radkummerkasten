#!/usr/bin/env python3


"""Look up the closest street address for a pair of coordinates."""

import os
import pathlib

import geopandas
import shapely

__all__ = [
    "AddressLookup",
]


# Increase cache for faster sindex lookup
os.environ["OGR_SQLITE_CACHE"] = "128"


class AddressLookup:
    """Look up an address."""

    def __init__(self, data):
        """
        Create a simple gazetteer to look up addresses.

        Arguments
        ---------
        data : pathlib.Path
            path to a GPKG of Voronoi polygons around house numbers
        """
        # TODO: Add specific instructions on how to structure the voronoi data
        # file, possibly including sample code
        self.data = pathlib.Path(data).resolve()

    def lookup_address(self, lon, lat):
        """
        Look up an address from a pair of coordinates.

        Arguments
        ---------
        lon : float
            Longitude value of point coordinate for which to look up an
            address. (EPSG:4326)
        lat : float
            Latitude value of point coordinate for which to look up an address
            (EPSG:4326)
        """
        point = shapely.Point(lon, lat)
        try:
            record = geopandas.read_file(
                self.data,
                mask=point,
                rows=1,
            ).iloc[0]

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
