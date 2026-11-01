#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ['LocalEwbDataFilePaths']

from datetime import date
from pathlib import Path
from typing import Callable, Generator, Union, Any, Optional

from zepben.ewb import require
from zepben.ewb.database.paths.ewb_data_file_paths import EwbDataFilePaths


class LocalEwbDataFilePaths(EwbDataFilePaths):
    """Provides paths to all the various data files / folders in the local file system used by EWB."""

    def __init__(
        self,
        base_dir: Union[Path, str],
        create_path: bool = False,
        create_directories_func: Callable[[Path], Any] = lambda it: it.mkdir(parents=True),
        is_directory: Callable[[Path], bool] = Path.is_dir,
        exists: Callable[[Path], bool] = Path.exists,
        list_files: Callable[[Path], Generator[Path, None, None]] = Path.iterdir,
    ):
        """
        :param base_dir: The root directory of the EWB data structure.
        :param create_path: Create the root directory (and any missing parent folders) if it does not exist.
        :param create_directories_func: Function for directory creation.
        :param is_directory: Function to determine if the supplied path is a directory .
        :param exists: Function to determine if the supplied path exists.
        :param list_files: Function for listing directories and files under the supplied path.
        """
        self._base_dir = Path(base_dir)
        self._create_directories_func = create_directories_func
        self._exists = exists
        self._list_files = list_files

        if create_path:
            self._create_directories_func(base_dir)

        require(is_directory(base_dir), lambda: "base_dir must be a directory")

    def create_directories(self, database_date: date) -> Path:
        date_path = self._base_dir.joinpath(str(database_date))
        if not self._exists(date_path):
            self._create_directories_func(date_path)

        return date_path

    def enumerate_descendants(self, prefix: Optional[str] = None) -> Generator[Path, None, None]:
        """
        Lists the child items of source location, optionally scoped under a sub `prefix` of the base directory.

        :param prefix: An optional sub-directory (relative to the base directory) to enumerate under. When `None`, the whole
          source location is enumerated. Returns an empty iterator if the prefix doesn't exist.
        """
        target = self._base_dir.joinpath(prefix) if prefix is not None else self._base_dir
        if prefix is not None and not self._exists(target):
            return
        try:
            for it in self._list_files(target):
                yield it
        except FileNotFoundError:
            return

    def resolve_database(self, path: Path) -> Path:
        return self._base_dir.joinpath(path)
