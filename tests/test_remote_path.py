#!/usr/bin/env python


import datetime
import pathlib
import os

import radkummerkasten.utilities


class Test_RemotePath:
    def test_remote_path(self, some_online_file_url):
        remote_path = radkummerkasten.utilities.RemotePath(some_online_file_url)

        assert remote_path.exists()
        assert remote_path.name == pathlib.Path(some_online_file_url).name

        too_old = (
            datetime.datetime.now()
            - remote_path.max_cache_age
            - datetime.timedelta(seconds=1)
        )
        os.utime(
            f"{remote_path.cached_path}", (too_old.timestamp(), too_old.timestamp())
        )

        remote_path = radkummerkasten.utilities.RemotePath(some_online_file_url)

        assert datetime.datetime.fromtimestamp(remote_path.stat().st_mtime) > too_old
