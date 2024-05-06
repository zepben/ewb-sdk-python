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
        return self._base_dir

    def customer(self, model_date: date) -> Path:
        return self._to_dated_path(model_date, DatabaseType.CUSTOMER.fileDescriptor)

    def diagram(self, model_date: date) -> Path:
        return self._to_dated_path(model_date, DatabaseType.DIAGRAM.fileDescriptor)

    def measurement(self, model_date: date) -> Path:
        return self._to_dated_path(model_date, DatabaseType.MEASUREMENT.fileDescriptor)

    def networkModel(self, model_date: date) -> Path:
        return self._to_dated_path(model_date, DatabaseType.NETWORK_MODEL.fileDescriptor)

    def tileCache(self, model_date: date) -> Path:
        return self._to_dated_path(model_date, DatabaseType.TILE_CACHE.fileDescriptor)

    def energyReading(self, model_date: date) -> Path:
        return self._to_dated_path(model_date, DatabaseType.ENERGY_READING.fileDescriptor)

    def energyReadingsIndex(self, model_date: date) -> Path:
        return self._to_dated_path(model_date, DatabaseType.ENERGY_READINGS_INDEX.fileDescriptor)

    def loadAggregatorMetersByDate(self, model_date: date) -> Path:
        return self._to_dated_path(model_date, DatabaseType.LOAD_AGGREGATOR_METERS_BY_DATE.fileDescriptor)

    def weatherReading(self, model_date: date) -> Path:
        return self._to_dated_path(model_date, DatabaseType.WEATHER_READING.fileDescriptor)

    def resultsCache(self, model_date: date) -> Path:
        return self._to_dated_path(model_date, DatabaseType.RESULTS_CACHE.fileDescriptor)

    def createDirectories(self, model_date: date) -> Path:
        date_path = Path(str(self._base_dir), str(model_date))
        if self.exists(date_path):
            return date_path
        else:
            return self.create_directories(date_path)

    def _to_dated_path(self, model_date: date, file: str) -> Path:
        return Path(str(self._base_dir), str(model_date), f"{model_date}-{file}.sqlite")

    def check_exists(self, database_type: DatabaseType, model_date: date) -> bool:
        if not database_type.perDate:
            raise ValueError("INTERNAL ERROR: Should only be calling `checkExists` for `perDate` files.")

        if database_type == DatabaseType.CUSTOMER:
            model_path = self.customer(model_date)
        elif database_type == DatabaseType.DIAGRAM:
            model_path = self.diagram(model_date)
        elif database_type == DatabaseType.MEASUREMENT:
            model_path = self.measurement(model_date)
        elif database_type == DatabaseType.NETWORK_MODEL:
            model_path = self.networkModel(model_date)
        elif database_type == DatabaseType.TILE_CACHE:
            model_path = self.tileCache(model_date)
        elif database_type == DatabaseType.ENERGY_READING:
            model_path = self.energyReading(model_date)
        else:
            raise ValueError(
                "INTERNAL ERROR: Should only be calling `checkExists` for `perDate` files, which should all be covered above, so go ahead and add it.")
        return self.exists(model_path)

    def findClosest(self, database_type: DatabaseType, max_days_to_search: int = 999999, model_date: date = date.today(), search_forwards: bool = False) -> \
    Optional[date]:
        if not database_type.perDate:
            return None

        if self.check_exists(database_type, model_date):
            return model_date

        offset = 1

        while offset <= max_days_to_search:
            offset_days = timedelta(offset)
            try:
                previous_date = model_date - offset_days
                if self.check_exists(database_type, previous_date):
                    return previous_date
            except OverflowError:
                pass

            if search_forwards:
                try:
                    forward_date = model_date + offset_days
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
                    model_date = date.fromisoformat(file.name)
                    if self.exists(self._to_dated_path(model_date, database_type.fileDescriptor)):
                        to_return.append(model_date)
                except ValueError:
                    pass
        to_return.sort()
        return to_return

    def getNetworkModelDatabases(self) -> List[date]:
        return self._getAvailableDatesFor(DatabaseType.NETWORK_MODEL)
