#!/usr/bin/env python


import pytest


class Test_Tiles:
    @pytest.mark.parametrize(
        ("layer", "z", "x", "y", "expected_tile_pbf", "expected_http_status"),
        [
            (
                "radlkarte",
                12,
                2232,
                1420,
                "radlkarte-12-2232-1420",
                200,
            ),
            (
                "radlkarte",
                15,
                17875,
                11361,
                "radlkarte-15-17875-11361",
                200,
            ),
            (
                "radlkarte",
                17,
                71495,
                45454,
                "radlkarte-17-71495-45454",
                200,
            ),
            (
                "radlkarte",
                9,
                279,
                177,
                "radlkarte-9-279-177",
                200,
            ),
            (
                "radlkarte",
                15,
                25485,
                3673,
                "radlkarte-15-25485-3673",
                404,
            ),
            (
                "non-existing",
                12,
                345,
                678,
                "non-existing-12-345-678",
                404,
            ),
        ],
        indirect=["expected_tile_pbf"],
    )
    def test_tile_by_index(
        self, client, layer, z, x, y, expected_tile_pbf, expected_http_status
    ):
        response = client.get(f"/tiles/{layer}/{z}/{x}/{y}")
        assert response.status_code == expected_http_status
        assert response.get_data() == expected_tile_pbf

    def test_without_tile_layers(self, application_without_tile_layers):
        client = application_without_tile_layers.test_client()
        response = client.get("/tiles/layer/12/345/678")
        assert response.status_code == 404
