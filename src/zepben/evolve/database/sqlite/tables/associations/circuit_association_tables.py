#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import List

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.sqlite_table import SqliteTable

__all__ = ["TableCircuitsSubstations", "TableCircuitsTerminals"]


class TableCircuitsSubstations(SqliteTable):
    circuit_mrid: Column = None
    substation_mrid: Column = None

    def __init__(self):
        super(TableCircuitsSubstations, self).__init__()
        self.circuit_mrid = self._create_column("circuit_mrid", "TEXT", Nullable.NOT_NULL)
        self.substation_mrid = self._create_column("substation_mrid", "TEXT", Nullable.NOT_NULL)

    def name(self) -> str:
        return "circuits_substations"

    def unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableCircuitsSubstations, self).unique_index_columns()
        cols.append([self.circuit_mrid, self.substation_mrid])
        return cols

    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableCircuitsSubstations, self).non_unique_index_columns()
        cols.append([self.circuit_mrid])
        cols.append([self.substation_mrid])
        return cols


class TableCircuitsTerminals(SqliteTable):
    circuit_mrid: Column = None
    terminal_mrid: Column = None

    def __init__(self):
        super(TableCircuitsTerminals, self).__init__()
        self.circuit_mrid = self._create_column("circuit_mrid", "TEXT", Nullable.NOT_NULL)
        self.terminal_mrid = self._create_column("terminal_mrid", "TEXT", Nullable.NOT_NULL)

    def name(self) -> str:
        return "circuits_terminals"

    def unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableCircuitsTerminals, self).unique_index_columns()
        cols.append([self.circuit_mrid, self.terminal_mrid])
        return cols

    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableCircuitsTerminals, self).non_unique_index_columns()
        cols.append([self.circuit_mrid])
        cols.append([self.terminal_mrid])
        return cols
