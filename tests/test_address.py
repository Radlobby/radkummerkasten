#!/usr/bin/env python


import pytest


class Test_Address:
    @pytest.mark.parametrize(
        ("lon", "lat", "expected_address"),
        [
            # Radlobby Büro
            (
                16.3881797,
                48.2146238,
                {
                    "street": "Lichtenauergasse",
                    "housenumber": "4/1",
                    "postcode": "1020",
                    "city": "Wien",
                },
            ),
            # Argus Shop
            (
                16.36818147,
                48.19744061,
                {
                    "street": "Frankenberggasse",
                    "housenumber": "11",
                    "postcode": "1040",
                    "city": "Wien",
                },
            ),
            # nirgends
            (
                99.99,
                99.99,
                {
                    "error": "Address not found",
                },
            ),
            # Gemeinde ohne Straßennamen
            (
                13.2021693,
                46.9346755,
                {
                    "street": "Obervellach",
                    "housenumber": "77",
                    "postcode": "9821",
                    "city": "Obervellach",
                },
            ),
        ],
    )
    def test_address_by_coordinates(self, lon, lat, expected_address, client):
        response = client.get(f"/api/address/by-coordinates/{lon},{lat}")
        print(response.json)
        assert response.json == expected_address
