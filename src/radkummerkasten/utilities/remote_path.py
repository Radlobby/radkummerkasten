#!/usr/bin/env python3


"""A pathlib.Path to a cached copy of a remote resource."""


import datetime
import pathlib

import requests

try:
    import xdg_base_dirs
except ImportError:  # Python<3.10
    import xdg as xdg_base_dirs


__all__ = ["RemotePath"]


MAX_CACHE_AGE = datetime.timedelta(weeks=12)
PACKAGE = __name__.split(".")[0]


class RemotePath(pathlib.Path):
    """A pathlib.Path to a cached copy of a remote resource."""

    # decide which kind of pathlib.Path we are (Windows, Unix, ...)
    # cf. https://stackoverflow.com/a/66613346/463864
    try:
        _flavour = type(pathlib.Path())._flavour
    except AttributeError:  # Python>=3.13
        pass

    _CACHE_DIR = xdg_base_dirs.xdg_cache_home() / f"{PACKAGE}"

    def __new__(cls, remote_url, max_cache_age=MAX_CACHE_AGE):
        """Define a data set that is downloaded and cached on demand."""
        # pathlib.Path does everything in __new__, rather than __init__
        cached_path = cls._CACHE_DIR / pathlib.Path(remote_url).name
        return super().__new__(cls, cached_path)

    def __init__(self, remote_url, max_cache_age=MAX_CACHE_AGE):
        """
        Define a data set that is downloaded and cached on demand.

        Arguments
        ---------
        remote_url : str
            source URL for this data set
        max_cache_age : datetime.timedelta
            re-download the cached file after this time
        """
        cached_path = self._CACHE_DIR / pathlib.Path(remote_url).name

        try:  # Python>=3.12
            super().__init__(cached_path)
        except TypeError:
            super().__init__()

        self.remote_url = remote_url
        self.max_cache_age = max_cache_age
        self.cached_path = cached_path
        self._download_remote_file()

    def _download_remote_file(self):
        try:
            assert self.cached_path.exists()
            assert datetime.datetime.fromtimestamp(self.cached_path.stat().st_mtime) > (
                datetime.datetime.now() - self.max_cache_age
            )
        except AssertionError:
            self.cached_path.parent.mkdir(parents=True, exist_ok=True)
            with requests.get(self.remote_url) as response:
                self.cached_path.write_bytes(response.content)
