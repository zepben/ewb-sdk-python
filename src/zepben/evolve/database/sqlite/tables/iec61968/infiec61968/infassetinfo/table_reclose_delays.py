#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List, Generator

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.sqlite_table import SqliteTable


__all__ = ["TableRecloseDelays"]


class TableRecloseDelays(SqliteTable):

    def __init__(self):
        super().__init__()
        self.relay_info_mrid: Column = self._create_column("relay_info_mrid", "TEXT", Nullable.NOT_NULL)
        self.reclose_delay: Column = self._create_column("reclose_delay", "NUMBER", Nullable.NOT_NULL)
        self.sequence_number: Column = self._create_column("sequence_number", "INTEGER", Nullable.NOT_NULL)

    @property
    def name(self) -> str:
        return "reclose_delays"

    @property
    def unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().unique_index_columns
        yield [self.relay_info_mrid, self.sequence_number]

    @property
    def non_unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().non_unique_index_columns
        yield [self.relay_info_mrid]

    @property
    def select_sql(self):
        return f"{super().select_sql} ORDER BY relay_info_mrid, sequence_number ASC;"
