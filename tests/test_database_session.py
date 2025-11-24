#!/usr/bin/env python


"""Test the database session for radkummerkasten."""


import pytest

from radkummerkasten.database.models import Address


class TestDatabaseSession:
    """Test the database session object for radkummerkasten."""

    @pytest.mark.parametrize(
        ("street", "housenumber", "postcode", "municipality"),
        (("Biene-Maja-Straße", "27", 6969, "Gigritschpatschn"),),
    )
    def test_find_address(self, engine, street, housenumber, postcode, municipality):
        """Test radkummerkasten.database.models.Address."""
        with engine.session.begin() as session:
            address = Address(
                street,
                housenumber,
                postcode,
                municipality,
            )
            address_id = address.id
            session.add(address)
            session.commit()

        with engine.session.begin() as session:
            address = session.find(
                Address,
                street=street,
                housenumber=housenumber,
                postcode=postcode,
                municipality=municipality,
            )
            assert isinstance(address, Address)
            assert address.id == address_id

            session.rollback()

    @pytest.mark.parametrize(
        ("street", "housenumber", "postcode", "municipality"),
        (("Drohne-Willi-Straße", "11", 1234, "Bienenstock"),),
    )
    def test_find_unknown_address(
        self, engine, street, housenumber, postcode, municipality
    ):
        """Test radkummerkasten.database.models.Address."""
        with engine.session.begin() as session:
            address = session.find(
                Address,
                street=street,
                housenumber=housenumber,
                postcode=postcode,
                municipality=municipality,
            )
            assert address is None
            session.rollback()
