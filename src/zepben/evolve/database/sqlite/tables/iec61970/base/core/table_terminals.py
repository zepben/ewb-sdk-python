#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List, Generator

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_ac_dc_terminals import TableAcDcTerminals

__all__ = ["TableTerminals"]


class TableTerminals(TableAcDcTerminals):

    def __init__(self):
        super().__init__()
        self.conducting_equipment_mrid: Column = self._create_column("conducting_equipment_mrid", "TEXT", Nullable.NULL)
        self.sequence_number: Column = self._create_column("sequence_number", "INTEGER", Nullable.NOT_NULL)
        self.connectivity_node_mrid: Column = self._create_column("connectivity_node_mrid", "TEXT", Nullable.NULL)
        self.phases: Column = self._create_column("phases", "TEXT", Nullable.NOT_NULL)

    @property
    def name(self) -> str:
        return "terminals"

    @property
    def unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().unique_index_columns
        yield [self.conducting_equipment_mrid, self.sequence_number]

    @property
    def non_unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().non_unique_index_columns
        yield [self.connectivity_node_mrid]
