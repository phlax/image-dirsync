#!/usr/local/bin/python3

import os
import pathlib
import sys
import time
from functools import cached_property


class DirFsync:

    def __init__(self, src, dest):
        self._src = src
        self._dest = dest

    @cached_property
    def dest(self):
        return pathlib.Path(self._dest)

    @cached_property
    def src(self):
        return pathlib.Path(self._src)

    def fsync_file(self, file, f, waiting=False):
        if waiting:
            print(f"Waiting to sync file: {file.relative_to(self.dest)}")
            time.sleep(2)
        else:
            print(f"Fsync: {file.relative_to(self.dest)}")
        try:
            os.fsync(f)
        except PermissionError:
            self.fsync_file(file, f, waiting=True)

    def sync_file(self, src_file, dest_file):
        with dest_file.open("wb") as d:
            d.write(src_file.read_bytes())
            self.fsync_file(dest_file, d)

    # TODO: use asyncio/threads to sync in parallel
    def sync_dirs(self):
        for src_file in self.src.glob("**/*"):
            if src_file.is_dir():
                continue
            dest_file = self.dest.joinpath(src_file.relative_to(self.src))
            dest_file.parent.mkdir(exist_ok=True, parents=True)
            self.sync_file(src_file, dest_file)


def main(*args):
    DirFsync(*args).sync_dirs()


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
