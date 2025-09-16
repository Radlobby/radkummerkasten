#!/usr/bin/env python3


"""Test configuration options."""


from .default_configuration import DefaultConfiguration


class TestConfiguration(DefaultConfiguration):
    """Test configuration."""

    TESTING = True
