#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
__all__ = ["TableCurveData"]

from typing import List, Generator

from zepben.evolve import SqliteTable
from zepben.evolve.database.sqlite.tables.column import Column, Nullable


class TableCurveData(SqliteTable):
    """A class representing the CurveData columns required for the database table."""

    def __init__(self):
        super().__init__()
        self.curve_mrid: Column = self._create_column("curve_mrid", "TEXT", Nullable.NOT_NULL)
        """A column storing the curve mRID."""

        self.x_value: Column = self._create_column("x_value", "NUMBER", Nullable.NOT_NULL)
        """A column storing the xValue of this curve data point."""

        self.y1_value: Column = self._create_column("y1_value", "NUMBER", Nullable.NOT_NULL)
        """A column storing the y1Value of this curve data point."""

        self.y2_value: Column = self._create_column("y2_value", "NUMBER", Nullable.NULL)
        """A column storing the y2Value of this curve data point."""

        self.y3_value: Column = self._create_column("y3_value", "NUMBER", Nullable.NULL)
        """A column storing the y3Value of this curve data point."""

    @property
    def name(self) -> str:
        return "curve_data"

    @property
    def unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().unique_index_columns
        yield [self.curve_mrid, self.x_value]

    @property
    def non_unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().non_unique_index_columns
        yield [self.curve_mrid]
