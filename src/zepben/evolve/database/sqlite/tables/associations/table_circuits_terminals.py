#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List, Generator

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.sqlite_table import SqliteTable


__all__ = ["TableCircuitsTerminals"]


class TableCircuitsTerminals(SqliteTable):

    def __init__(self):
        super().__init__()
        self.circuit_mrid: Column = self._create_column("circuit_mrid", "TEXT", Nullable.NOT_NULL)
        self.terminal_mrid: Column = self._create_column("terminal_mrid", "TEXT", Nullable.NOT_NULL)

    @property
    def name(self) -> str:
        return "circuits_terminals"

    @property
    def unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().unique_index_columns
        yield [self.circuit_mrid, self.terminal_mrid]

    @property
    def non_unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().non_unique_index_columns
        yield [self.circuit_mrid]
        yield [self.terminal_mrid]
