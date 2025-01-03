#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List, Generator

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.sqlite_table import SqliteTable

__all__ = ["TableEndDevicesEndDeviceFunctions"]


class TableEndDevicesEndDeviceFunctions(SqliteTable):
    """
    A class representing the association between EndDevices and EndDeviceFunctions.
    """

    def __init__(self):
        super().__init__()
        self.end_device_mrid: Column = self._create_column("end_device_mrid", "TEXT", Nullable.NOT_NULL)
        """A column storing the mRID of EndDevices."""

        self.end_device_function_mrid: Column = self._create_column("end_device_function_mrid", "TEXT", Nullable.NOT_NULL)
        """A column storing the mRID of EndDeviceFunctions."""

    @property
    def name(self) -> str:
        return "end_devices_end_device_functions"

    @property
    def unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().unique_index_columns
        yield [self.end_device_mrid, self.end_device_function_mrid]

    @property
    def non_unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().non_unique_index_columns
        yield [self.end_device_mrid]
        yield [self.end_device_function_mrid]
