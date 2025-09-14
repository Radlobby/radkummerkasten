#!/usr/bin/env python3


"""A custom build backend that also compiles SASS and ECMA-script."""


import functools
import pathlib
import tomllib

import setuptools.build_meta
from setuptools.build_meta import *


BUILD_REQUIREMENTS = [
    "libsass",
]


@functools.cache
def _configuration():
    with (pathlib.Path.cwd() / "pyproject.toml").open("rb") as f:
        configuration = tomllib.load(f)["tools"]["radkummerkasten-build-backend"]
    return configuration


def _find_sass_files():
    return [
        pathlib.Path(sass_file) 
        for sass_file
        in _configuration()["sass_files"]
    ]


def _compile_sass_file(input_filename):
    import sass
    output_filename = input_filename.with_suffix(".min.css")
    with output_filename.open("w") as f:
        f.write(sass.compile(filename=f"{input_filename}", output_style="compressed"))
    return output_filename


def build_sass(f):
    # 1. compile sass files (remember outputs)
    # 2. run f()
    # 3. rm outputs from 1
    def wrapper(*args, **kwargs):
        compiled_sass_files = [
            _compile_sass_file(sass_file) for sass_file in _find_sass_files()
        ]
        results = f(*args, **kwargs)
        [compiled_sass_file.unlink() for compiled_sass_file in compiled_sass_files]
        return results

    return wrapper


@build_sass
def build_editable(wheel_directory, config_settings=None, metadata_directory=None):
    return setuptools.build_meta.build_editable(
        wheel_directory, config_settings, metadata_directory
    )


@build_sass
def build_sdist(sdist_directory, config_settings=None):
    print("SDIST", sdist_directory, "/SDIST")
    return setuptools.build_meta.build_sdist(sdist_directory, config_settings)


@build_sass
def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    print("WHEEL", wheel_directory, config_settings, metadata_directory, "/WHEEL")
    import subprocess

    subprocess.call(["ls", "-alhtr", wheel_directory])
    return setuptools.build_meta.build_wheel(
        wheel_directory, config_settings, metadata_directory
    )


def get_requires_for_build_editable(config_settings=None):
    return BUILD_REQUIREMENTS


def get_requires_for_build_sdist(config_settings=None):
    return BUILD_REQUIREMENTS


def get_requires_for_build_wheel(config_settings=None):
    return BUILD_REQUIREMENTS
