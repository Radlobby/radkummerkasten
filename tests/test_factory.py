#!/usr/bin/env python


"""Test the application factory of radkummerkasten."""


import os

import pytest

import radkummerkasten


class TestFactory:
    """Test the application factory of radkummerkasten."""

    def test_create_app(self, instance_directory):
        """Test the application factory of radkummerkasten."""
        _ = radkummerkasten.create_app(instance_path=instance_directory)

    def test_create_app_without_testing_envvar(self, instance_directory):
        """Test the application factory of radkummerkasten."""
        try:
            del os.environ["TESTING"]
        except KeyError:
            pass
        _ = radkummerkasten.create_app(instance_path=instance_directory)

    @pytest.mark.parametrize(
        ("env_testing_value",),
        [
            (0,),
            ("0",),
            ("FALSE",),
            ("oFf",),
            (1,),
            ("true",),
            ("on",),
            ("FOOBAR",),
        ],
    )
    def test_create_app_with_testing_env(self, instance_directory, env_testing_value):
        """Test the application factory of radkummerkasten."""
        os.environ["TESTING"] = f"{env_testing_value}"
        _ = radkummerkasten.create_app(instance_path=instance_directory)
