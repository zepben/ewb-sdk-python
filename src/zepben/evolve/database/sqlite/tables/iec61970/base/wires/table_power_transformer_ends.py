#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List, Generator

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_transformer_ends import TableTransformerEnds

__all__ = ["TablePowerTransformerEnds"]


class TablePowerTransformerEnds(TableTransformerEnds):

    def __init__(self):
        super().__init__()
        self.power_transformer_mrid: Column = self._create_column("power_transformer_mrid", "TEXT", Nullable.NULL)
        self.connection_kind: Column = self._create_column("connection_kind", "TEXT", Nullable.NOT_NULL)
        self.phase_angle_clock: Column = self._create_column("phase_angle_clock", "INTEGER", Nullable.NULL)
        self.b: Column = self._create_column("b", "NUMBER", Nullable.NULL)
        self.b0: Column = self._create_column("b0", "NUMBER", Nullable.NULL)
        self.g: Column = self._create_column("g", "NUMBER", Nullable.NULL)
        self.g0: Column = self._create_column("g0", "NUMBER", Nullable.NULL)
        self.r: Column = self._create_column("r", "NUMBER", Nullable.NULL)
        self.r0: Column = self._create_column("r0", "NUMBER", Nullable.NULL)
        self.rated_u: Column = self._create_column("rated_u", "INTEGER", Nullable.NULL)
        self.x: Column = self._create_column("x", "NUMBER", Nullable.NULL)
        self.x0: Column = self._create_column("x0", "NUMBER", Nullable.NULL)

    @property
    def name(self) -> str:
        return "power_transformer_ends"

    @property
    def unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().unique_index_columns
        yield [self.power_transformer_mrid, self.end_number]

    @property
    def non_unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().non_unique_index_columns
        yield [self.power_transformer_mrid]
