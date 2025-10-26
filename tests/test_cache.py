#!/usr/bin/env python


import pytest


class TestCache:
    @pytest.mark.parametrize(
        ("key", "value"),
        [
            ("foo", b"bar"),
        ],
    )
    def test_cache(self, cache, key, value):
        cache[key] = value
        assert cache[key] == value
