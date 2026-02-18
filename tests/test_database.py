#!/usr/bin/env python


"""Test the database interface."""

import pytest

from radkummerkasten.database import Database


class TestDatabase:
    """Test the database interface."""

    def test_init_app_a_second_time(self, application):
        """Test the database interface."""
        with pytest.raises(RuntimeError):
            _ = Database(application)
