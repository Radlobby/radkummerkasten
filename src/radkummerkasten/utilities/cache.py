#!/usr/bin/env python3


"""A mechanism for caching files."""


import datetime

try:
    import xdg_base_dirs
except ImportError:  # Python<3.10
    import xdg as xdg_base_dirs


__all__ = ["Cache"]


PACKAGE = __name__.split(".")[0]


class Cache:
    """A mechanism for caching files."""

    CACHE_DIR = xdg_base_dirs.xdg_cache_home() / f"{PACKAGE}"

    def __init__(self, name, max_cache_age=datetime.timedelta(weeks=1)):
        """
        Initialise a cache.

        Arguments
        ---------
        name : str
            A freetext realm for this cache
        max_cache_age : datetime.timedelta
            Delete files from the cache that are older than max_cache_age.
            Default: one week
        """
        self.name = name
        self.max_cache_age = max_cache_age

    def __enter__(self):
        """Enter a cache context."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Leave a cache context."""
        pass

    def __getitem__(self, key):
        """Fetch item from cache (or None)."""
        cache_path = self._cache_path_for(key)
        try:
            value = cache_path.read_bytes()
            self.expire(key)
        except FileNotFoundError:
            value = None
        return value

    def __setitem__(self, key, value):
        """Store value in cache."""
        cache_path = self._cache_path_for(key)
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_bytes(value)

    def _cache_path_for(self, key):
        cache_path = self.CACHE_DIR / key
        try:
            assert cache_path.is_relative_to(self.CACHE_DIR)
        except AssertionError:
            raise RuntimeError("Cache keys cannot be absolute or parent paths")
        return cache_path

    def expire(self, key):
        """Expire a cached item."""
        cache_path = self._cache_path_for(key)
        if (
            datetime.datetime.fromtimestamp(cache_path.stat().st_mtime)
            > (datetime.datetime.now() - self.max_cache_age)
        ):
            cache_path.unlink()
