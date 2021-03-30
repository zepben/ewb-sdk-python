#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from enum import Enum
from typing import List

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.sqlite_table import SqliteTable

__all__ = ["LoopSubstationRelationship", "TableLoopsSubstations"]


class LoopSubstationRelationship(Enum):
    SUBSTATION_ENERGIZES_LOOP = 0
    LOOP_ENERGIZES_SUBSTATION = 1


class TableLoopsSubstations(SqliteTable):
    loop_mrid: Column = None
    substation_mrid: Column = None
    relationship: Column = None

    def __init__(self):
        super().__init__()
        self.column_index += 1
        self.loop_mrid = Column(self.column_index, "loop_mrid", "TEXT", Nullable.NOT_NULL)
        self.column_index += 1
        self.substation_mrid = Column(self.column_index, "substation_mrid", "TEXT", Nullable.NOT_NULL)
        self.column_index += 1
        self.relationship = Column(self.column_index, "relationship", "TEXT", Nullable.NOT_NULL)

    def name(self) -> str:
        return "loops_substations"

    def unique_index_columns(self) -> List[List[Column]]:
        cols = super().unique_index_columns()
        cols.append([self.loop_mrid, self.substation_mrid])
        return cols

    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super().non_unique_index_columns()
        cols.append([self.loop_mrid])
        cols.append([self.substation_mrid])
        return cols

