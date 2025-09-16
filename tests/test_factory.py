#!/usr/bin/env python


import os

import pytest

import radkummerkasten


class Test_Factory:
    def test_create_app(self, test_instance_directory):
        _ = radkummerkasten.create_app(instance_path=test_instance_directory)

    def test_create_app_without_testing_envvar(self, test_instance_directory):
        try:
            del os.environ["TESTING"]
        except KeyError:
            pass
        _ = radkummerkasten.create_app(instance_path=test_instance_directory)

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
        ]
    )
    def test_create_app_with_testing_env(self, test_instance_directory, env_testing_value):
        os.environ["TESTING"] = "0"
        _ = radkummerkasten.create_app(instance_path=test_instance_directory)
