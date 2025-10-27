#!/usr/bin/env python


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
