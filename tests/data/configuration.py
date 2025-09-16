#!/usr/bin/env python3


"""Define configuration options for testing radkummerkasten."""


from radkummerkasten.configuration import TestConfiguration


class Configuration(TestConfiguration):
    """Configuration for testing radkummerkasten."""

    tile_layers = [
        "radlkarte-wien.geojson",
    ]
