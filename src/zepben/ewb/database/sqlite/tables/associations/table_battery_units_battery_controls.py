#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["TableBatteryUnitsBatteryControls"]

from typing import List, Generator

from zepben.ewb.database.sql.column import Column, Nullable
from zepben.ewb.database.sqlite.tables.sqlite_table import SqliteTable


class TableBatteryUnitsBatteryControls(SqliteTable):
    """
    A class representing the association between BatteryUnits and BatteryControls.
    """

    def __init__(self):
        super().__init__()
        self.battery_unit_mrid: Column = self._create_column("battery_unit_mrid", "TEXT", Nullable.NOT_NULL)
        """A column storing the mRID of BatteryUnits."""

        self.battery_control_mrid: Column = self._create_column("battery_control_mrid", "TEXT", Nullable.NOT_NULL)
        """A column storing the mRID of BatteryControls."""

    @property
    def name(self) -> str:
        return "battery_units_battery_controls"

    @property
    def unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().unique_index_columns
        yield [self.battery_unit_mrid, self.battery_control_mrid]

    @property
    def non_unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().non_unique_index_columns
        yield [self.battery_unit_mrid]
        yield [self.battery_control_mrid]
