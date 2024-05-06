#  Copyright 2024 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from datetime import date
from pathlib import Path
from typing import Callable, Iterator, Optional, List

from zepben.evolve import require
from zepben.evolve.database.paths.database_type import DatabaseType

__all__ = ['EwbDataFilePaths']


class EwbDataFilePaths:
    baseDir: Path = None
    createDirectories: Callable[[Path], Path] = None
    isDirectory: Callable[[Path], bool] = None
    exists: Callable[[Path], bool] = None
    listsFiles: Callable[[Path], Iterator[Path]] = None

    def __init__(self, baseDir: Path = Path("/tmp/"),
                 createPath: bool = False,
                 createDirectories: Callable[[Path], Path] = lambda it: it.mkdir(parents=True),
                 isDirectory: Callable[[Path], bool] = Path.is_dir,
                 exists: Callable[[Path], bool] = Path.exists,
                 listsFiles: Callable[[Path], Iterator[Path]] = Path.iterdir):

        if createDirectories is not None:
            self.createDirectories = createDirectories
        if isDirectory is not None:
            self.isDirectory = isDirectory
        if exists is not None:
            self.exists = exists
        if listsFiles is not None:
            self.listsFiles = listsFiles
        if baseDir is not None:
            self.baseDir = baseDir

        if createPath:
            self.createDirectories(baseDir)

        require(self.isDirectory(baseDir), lambda: f"baseDir must be a directory")



    def customer(self, date: datetime.date) -> Path:
        return self._to_dated_path(date, DatabaseType.CUSTOMER.fileDescriptor)

    def diagram(self, date: datetime.date) -> Path:
        return self._to_dated_path(date, DatabaseType.DIAGRAM.fileDescriptor)

    def measurement(self, date: datetime.date) -> Path:
        return self._to_dated_path(date, DatabaseType.MEASUREMENT.fileDescriptor)

    def networkModel(self, date: datetime.date) -> Path:
        return self._to_dated_path(date, DatabaseType.NETWORK_MODEL.fileDescriptor)

    def tileCache(self, date: datetime.date) -> Path:
        return self._to_dated_path(date, DatabaseType.TILE_CACHE.fileDescriptor)

    def energyReading(self, date: datetime.date) -> Path:
        return self._to_dated_path(date, DatabaseType.ENERGY_READING.fileDescriptor)

    def energyReadingsIndex(self, date: datetime.date) -> Path:
        return self._to_dated_path(date, DatabaseType.ENERGY_READINGS_INDEX.fileDescriptor)

    def loadAggregatorMetersByDate(self, date: datetime.date) -> Path:
        return self._to_dated_path(date, DatabaseType.LOAD_AGGREGATOR_METERS_BY_DATE.fileDescriptor)

    def weatherReading(self, date: datetime.date) -> Path:
        return self._to_dated_path(date, DatabaseType.WEATHER_READING.fileDescriptor)

    def resultsCache(self, date: datetime.date) -> Path:
        return self._to_dated_path(date, DatabaseType.RESULTS_CACHE.fileDescriptor)

    def createDirectories2(self, date: datetime.date) -> Path:
        datePath = Path(str(self.baseDir), str(date))
        if self.exists(datePath):
            return datePath
        else:
            return self.createDirectories(datePath)

    def _to_dated_path(self, date: datetime.date, file: str) -> Path:
        return Path(str(self.baseDir), str(date), f"{date}-{file}.sqlite")

    def check_exists(self, type: DatabaseType, date: datetime.date) -> bool:
        if not type.perDate:
            raise ValueError("INTERNAL ERROR: Should only be calling `checkExists` for `perDate` files.")

        if type == DatabaseType.CUSTOMER:
            model_path = self.customer(date)
        elif type == DatabaseType.DIAGRAM:
            model_path = self.diagram(date)
        elif type == DatabaseType.MEASUREMENT:
            model_path = self.measurement(date)
        elif type == DatabaseType.NETWORK_MODEL:
            model_path = self.networkModel(date)
        elif type == DatabaseType.TILE_CACHE:
            model_path = self.tileCache(date)
        elif type == DatabaseType.ENERGY_READING:
            model_path = self.energyReading(date)
        else:
            raise ValueError(
                "INTERNAL ERROR: Should only be calling `checkExists` for `perDate` files, which should all be covered above, so go ahead and add it.")
        return self.exists(model_path)

    def findClosest(self, type: DatabaseType, maxDaysToSearch: int = 999999, date: datetime.date = datetime.date.today(), searchForwards: bool = False) -> Optional[datetime.date]:
        if not type.perDate:
            return None

        if self.check_exists(type, date):
            return date

        offset = 1

        while offset <= maxDaysToSearch:
            offset_days = datetime.timedelta(offset)
            try:
                previous_date = date - offset_days
                if self.check_exists(type, previous_date):
                    return previous_date
            except OverflowError as e:
                pass

            if searchForwards:
                try:
                    forward_date = date + offset_days
                    if self.check_exists(type, forward_date):
                        return forward_date
                except OverflowError as e:
                    pass
            offset += 1
        return None

    def _getAvailableDatesFor(self, type: DatabaseType) -> List[datetime.date]:
        if not type.perDate:
            raise ValueError(
                "INTERNAL ERROR: Should only be calling `getAvailableDatesFor` for `perDate` files.")

        to_return = list()

        for file in self.listsFiles(self.baseDir):
            if self.isDirectory(file):
                try:
                    date = datetime.date.fromisoformat(file.name)
                    if self.exists(self._to_dated_path(date, type.fileDescriptor)):
                        to_return.append(date)
                except ValueError:
                    pass
        to_return.sort()
        return to_return

    def getNetworkModelDatabases(self) -> List[datetime.date]:
        return self._getAvailableDatesFor(DatabaseType.NETWORK_MODEL)
