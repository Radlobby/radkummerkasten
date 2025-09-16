#!/usr/bin/env python3


"""Test configuration options."""


from .base_configuration import BaseConfiguration


class TestConfiguration(BaseConfiguration):
    """Test configuration."""

    TESTING = True
