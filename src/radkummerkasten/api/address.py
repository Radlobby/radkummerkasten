#!/usr/bin/env python3


"""Look up the closest street address for a pair of coordinates."""


import flask

from ..core import AddressLookup
from ..utilities.decorators import local_referer_only

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

    def __init__(self, configuration, *args, **kwargs):
        """Provide a blueprint for address lookup."""
        kwargs = kwargs or {}
        kwargs.update(self._kwargs)
        super().__init__(self._NAME, self._IMPORT_NAME, *args, **kwargs)

        try:
            self._address_lookup = AddressLookup(configuration["ADDRESS_LOOKUP_LAYER"])
        except KeyError:
            self._address_lookup = None

        self.add_url_rule(
            "/by-coordinates/<float:lon>,<float:lat>",
            view_func=self.look_up_address,
            methods=("GET",),
        )

    @local_referer_only
    def look_up_address(self, lon, lat):
        """Look up an address from a pair of coordinates."""
        if self._address_lookup is None:
            address = {"error": "Address not found"}
        else:
            address = self._address_lookup.lookup_address(lon, lat)
        return flask.jsonify(address)
