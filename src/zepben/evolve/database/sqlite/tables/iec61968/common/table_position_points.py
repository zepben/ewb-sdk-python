#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List, Generator

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.sqlite_table import SqliteTable


__all__ = ["TablePositionPoints"]


class TablePositionPoints(SqliteTable):

    def __init__(self):
        super().__init__()
        self.location_mrid: Column = self._create_column("location_mrid", "TEXT", Nullable.NOT_NULL)
        self.sequence_number: Column = self._create_column("sequence_number", "INTEGER", Nullable.NOT_NULL)
        self.x_position: Column = self._create_column("x_position", "NUMBER", Nullable.NOT_NULL)
        self.y_position: Column = self._create_column("y_position", "NUMBER", Nullable.NOT_NULL)

    @property
    def name(self) -> str:
        return "position_points"

    @property
    def unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().unique_index_columns
        yield [self.location_mrid, self.sequence_number]
