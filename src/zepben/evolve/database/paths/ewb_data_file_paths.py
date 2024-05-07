#  Copyright 2024 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from datetime import date, timedelta
from pathlib import Path
from typing import Callable, Iterator, Optional, List

from zepben.evolve import require
from zepben.evolve.database.paths.database_type import DatabaseType

__all__ = ['EwbDataFilePaths']


class EwbDataFilePaths:
    """Provides paths to all the various data files / folders used by EWB."""
    _base_dir: Path = None
    create_directories: Callable[[Path], Path] = None
    is_directory: Callable[[Path], bool] = None
    exists: Callable[[Path], bool] = None
    list_files: Callable[[Path], Iterator[Path]] = None

    def __init__(self, base_dir: Path,
                 create_path: bool = False,
                 create_directories: Callable[[Path], Path] = lambda it: it.mkdir(parents=True),
                 is_directory: Callable[[Path], bool] = Path.is_dir,
                 exists: Callable[[Path], bool] = Path.exists,
                 list_files: Callable[[Path], Iterator[Path]] = Path.iterdir):
        """
        :param: base_dir The root directory of the EWB data structure.
        :param: createPath Create the root directory (and any missing parent folders) if it does not exist.
        """

        if create_directories is not None:
            self.create_directories = create_directories
        if is_directory is not None:
            self.is_directory = is_directory
        if exists is not None:
            self.exists = exists
        if list_files is not None:
            self.list_files = list_files
        if base_dir is not None:
            self._base_dir = base_dir

        if create_path:
            self.create_directories(base_dir)

        require(self.is_directory(base_dir), lambda: f"baseDir must be a directory")

    @property
    def baseDir(self):
        """The root directory of the EWB data structure."""
        return self._base_dir

    def customer(self, database_date: date) -> Path:
        """
        Determine the path to the "customers" database for the specified date.

        :param database_date: The :class:`date` to use for the "customers" database.
        :return: The :class:`path` to the "customers" database for the specified date.
        """
        return self._to_dated_path(database_date, DatabaseType.CUSTOMER.fileDescriptor)

    def diagram(self, database_date: date) -> Path:
        """
        Determine the path to the "diagrams" database for the specified date.

        :param database_date: The :class:`date` to use for the "diagrams" database.
        :return: The :class:`path` to the "diagrams" database for the specified date.
        """
        return self._to_dated_path(database_date, DatabaseType.DIAGRAM.fileDescriptor)

    def measurement(self, database_date: date) -> Path:
        """
        Determine the path to the "measurements" database for the specified date.

        :param database_date: The :class:`date` to use for the "measurements" database.
        :return: The :class:`path` to the "measurements" database for the specified date.
        """
        return self._to_dated_path(database_date, DatabaseType.MEASUREMENT.fileDescriptor)

    def networkModel(self, database_date: date) -> Path:
        """
        Determine the path to the "network model" database for the specified date.

        :param database_date: The :class:`date` to use for the "network model" database.
        :return: The :class:`path` to the "network model" database for the specified date.
        """
        return self._to_dated_path(database_date, DatabaseType.NETWORK_MODEL.fileDescriptor)

    def tileCache(self, database_date: date) -> Path:
        """
        Determine the path to the "tile cache" database for the specified date.

        :param database_date: The :class:`date` to use for the "tile cache" database.
        :return: The :class:`path` to the "tile cache" database for the specified date.
        """
        return self._to_dated_path(database_date, DatabaseType.TILE_CACHE.fileDescriptor)

    def energyReading(self, database_date: date) -> Path:
        """
        Determine the path to the "energy readings" database for the specified date.

        :param database_date: The :class:`date` to use for the "energy readings" database.
        :return: The :class:`path` to the "energy readings" database for the specified date.
        """
        return self._to_dated_path(database_date, DatabaseType.ENERGY_READING.fileDescriptor)

    def energyReadingsIndex(self, database_date: date) -> Path:
        """
        Determine the path to the "energy readings index" database.

        :return: The :class:`path` to the "energy readings index" database.
        """
        return self._to_dated_path(database_date, DatabaseType.ENERGY_READINGS_INDEX.fileDescriptor)

    def loadAggregatorMetersByDate(self, database_date: date) -> Path:
        """
        Determine the path to the "load aggregator meters-by-date" database.

        :return: The :class:`path` to the "load aggregator meters-by-date" database.
        """
        return self._to_dated_path(database_date, DatabaseType.LOAD_AGGREGATOR_METERS_BY_DATE.fileDescriptor)

    def weatherReading(self, database_date: date) -> Path:
        """
        Determine the path to the "weather readings" database.

        :return: The :class:`path` to the "weather readings" database.
        """
        return self._to_dated_path(database_date, DatabaseType.WEATHER_READING.fileDescriptor)

    def resultsCache(self, database_date: date) -> Path:
        """
        Determine the path to the "results cache" database.

        :return: The :class:`path` to the "results cache" database.
        """
        return self._to_dated_path(database_date, DatabaseType.RESULTS_CACHE.fileDescriptor)

    def createDirectories(self, database_date: date) -> Path:
        """
        Create the directories required to have a valid path for the specified date.

        :param database_date: The :class:`date` required in the path.
        :return: The :class:`path` to the directory for the `database_date`.
        """
        date_path = Path(str(self._base_dir), str(database_date))
        if self.exists(date_path):
            return date_path
        else:
            return self.create_directories(date_path)

    def _to_dated_path(self, database_date: date, file: str) -> Path:
        return Path(str(self._base_dir), str(database_date), f"{database_date}-{file}.sqlite")

    def check_exists(self, database_type: DatabaseType, database_date: date) -> bool:
        """
        Check if a database of the specified type and date exists.

        :param database_type: The type of database to search for.
        :param database_date: The date to check.
        :return: `True` if a database of the specified `database_type` and `database_date` exists in the date path.
        """
        if not database_type.perDate:
            raise ValueError("INTERNAL ERROR: Should only be calling `checkExists` for `perDate` files.")

        if database_type == DatabaseType.CUSTOMER:
            model_path = self.customer(database_date)
        elif database_type == DatabaseType.DIAGRAM:
            model_path = self.diagram(database_date)
        elif database_type == DatabaseType.MEASUREMENT:
            model_path = self.measurement(database_date)
        elif database_type == DatabaseType.NETWORK_MODEL:
            model_path = self.networkModel(database_date)
        elif database_type == DatabaseType.TILE_CACHE:
            model_path = self.tileCache(database_date)
        elif database_type == DatabaseType.ENERGY_READING:
            model_path = self.energyReading(database_date)
        else:
            raise ValueError(
                "INTERNAL ERROR: Should only be calling `checkExists` for `perDate` files, which should all be covered above, so go ahead and add it.")
        return self.exists(model_path)

    def findClosest(self, database_type: DatabaseType, max_days_to_search: int = 999999, start_date: date = date.today(), search_forwards: bool = False) -> \
        Optional[date]:
        """
        Find the closest date with a usable database of the specified type.

        :param database_type: The type of database to search for.
        :param max_days_to_search: The maximum number of days to search for a valid database.
        :param start_date: The target :class:`date`. Defaults to today.
        :param search_forwards: Indicates the search should also look forwards in time from `start_date` for a valid file. Defaults to reverse search only.
        :return: The closest :class:`date` to `database_date` with a valid database of `database_type` within the search parameters, or `None` if no valid database was found.
        """
        if not database_type.perDate:
            return None

        if self.check_exists(database_type, start_date):
            return start_date

        offset = 1

        while offset <= max_days_to_search:
            offset_days = timedelta(offset)
            try:
                previous_date = start_date - offset_days
                if self.check_exists(database_type, previous_date):
                    return previous_date
            except OverflowError:
                pass

            if search_forwards:
                try:
                    forward_date = start_date + offset_days
                    if self.check_exists(database_type, forward_date):
                        return forward_date
                except OverflowError:
                    pass
            offset += 1
        return None

    def _getAvailableDatesFor(self, database_type: DatabaseType) -> List[date]:
        if not database_type.perDate:
            raise ValueError(
                "INTERNAL ERROR: Should only be calling `getAvailableDatesFor` for `perDate` files.")

        to_return = list()

        for file in self.list_files(self._base_dir):
            if self.is_directory(file):
                try:
                    database_date = date.fromisoformat(file.name)
                    if self.exists(self._to_dated_path(database_date, database_type.fileDescriptor)):
                        to_return.append(database_date)
                except ValueError:
                    pass
        to_return.sort()
        return to_return

    def getNetworkModelDatabases(self) -> List[date]:
        """
        Find available network-model databases in data path.

        :return: A list of :class:`date`'s for which network-model databases exist in the data path.
        """
        return self._getAvailableDatesFor(DatabaseType.NETWORK_MODEL)
