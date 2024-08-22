#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List, Generator

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.sqlite_table import SqliteTable


__all__ = ["TableEquipmentUsagePoints"]


class TableEquipmentUsagePoints(SqliteTable):
    """
    A class representing the association between Equipment and UsagePoints.
    """

    def __init__(self):
        super().__init__()
        self.equipment_mrid: Column = self._create_column("equipment_mrid", "TEXT", Nullable.NOT_NULL)
        """A column storing the mRID of Equipment."""

        self.usage_point_mrid: Column = self._create_column("usage_point_mrid", "TEXT", Nullable.NOT_NULL)
        """A column storing the mRID of UsagePoints."""

    @property
    def name(self) -> str:
        return "equipment_usage_points"

    @property
    def unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().unique_index_columns
        yield [self.equipment_mrid, self.usage_point_mrid]

    @property
    def non_unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().non_unique_index_columns
        yield [self.equipment_mrid]
        yield [self.usage_point_mrid]
