#!/usr/bin/env python3


"""Define configuration options for testing radkummerkasten."""


import pathlib

_DATA_DIR = pathlib.Path(__file__).parent


TILE_LAYERS = {
    "radlkarte": (_DATA_DIR / "radlkarte-wien.geojson").absolute(),
}
