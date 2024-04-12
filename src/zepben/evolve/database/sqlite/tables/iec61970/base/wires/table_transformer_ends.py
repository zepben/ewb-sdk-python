#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from abc import ABC
from typing import List, Generator

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_identified_objects import TableIdentifiedObjects

__all__ = ["TableTransformerEnds"]


class TableTransformerEnds(TableIdentifiedObjects, ABC):

    def __init__(self):
        super().__init__()
        self.end_number: Column = self._create_column("end_number", "INTEGER", Nullable.NOT_NULL)
        self.terminal_mrid: Column = self._create_column("terminal_mrid", "TEXT", Nullable.NULL)
        self.base_voltage_mrid: Column = self._create_column("base_voltage_mrid", "TEXT", Nullable.NULL)
        self.grounded: Column = self._create_column("grounded", "BOOLEAN", Nullable.NOT_NULL)
        self.r_ground: Column = self._create_column("r_ground", "NUMBER", Nullable.NULL)
        self.x_ground: Column = self._create_column("x_ground", "NUMBER", Nullable.NULL)
        self.star_impedance_mrid: Column = self._create_column("star_impedance_mrid", "TEXT", Nullable.NULL)

    @property
    def non_unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().non_unique_index_columns
        yield [self.star_impedance_mrid]
