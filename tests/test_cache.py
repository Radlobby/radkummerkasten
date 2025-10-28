#!/usr/bin/env python


import datetime
import pathlib
import os

import pytest


class TestBytesCache:
    @pytest.mark.parametrize(
        ("key", "value"),
        [
            ("foo", b"bar"),
        ],
    )
    def test_cache(self, cache, key, value):
        cache[key] = value
        assert cache[key] == value

    def test_cache_no_absolute_path(self, cache):
        with pytest.raises(
            AssertionError, match="Cache keys cannot be absolute or parent paths"
        ):
            cache["/etc/passwd"] = "FOOBAR"

    def test_cache_no_parent_path(self, cache):
        with pytest.raises(
            AssertionError, match="Cache keys cannot be absolute or parent paths"
        ):
            cache["../../etc/passwd"] = "FOOBAR"

    @pytest.mark.parametrize(
        ("path", "subpath", "expected_value"),
        [
            (pathlib.Path("/tmp/"), pathlib.Path("/tmp/abc.txt"), True),
            (pathlib.Path("/tmp/"), pathlib.Path("/etc/passwd"), False),
            (pathlib.Path("/tmp/"), pathlib.Path("../../../etc/passwd"), False),
        ],
    )
    def test_is_subpath(self, cache, path, subpath, expected_value):
        assert cache._is_subpath(path, subpath) == expected_value

    @pytest.mark.parametrize(
        ("key", "value"),
        [
            ("foo", b"bar"),
        ],
    )
    def test_expire_by_age(self, cache, key, value):
        cache[key] = value
        EXPIRED = (
            datetime.datetime.now()
            - cache.max_cache_age
            - datetime.timedelta(days=1)
        ).timestamp()
        os.utime(cache._cache_path_for(key), (EXPIRED, EXPIRED))

        # when accessing a file that is older than max_cache_age/EXPIRED,
        # it is returned but invalidated afterwards

        # fetch it once: returns a valid response
        assert cache[key] == value

        # fetch it another time: key error
        with pytest.raises(KeyError):
            _ = cache[key]

    @pytest.mark.parametrize(
        ("key", "value"),
        [
            ("foo", b"bar"),
        ],
    )
    def test_expire_now(self, cache, key, value):
        cache[key] = value
        cache.expire(key, now=True)
        with pytest.raises(KeyError):
            _ = cache[key]
