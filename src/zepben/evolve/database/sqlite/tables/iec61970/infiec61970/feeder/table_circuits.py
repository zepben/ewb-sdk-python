#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List, Generator

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_lines import TableLines

__all__ = ["TableCircuits"]


class TableCircuits(TableLines):

    def __init__(self):
        super().__init__()
        self.loop_mrid: Column = self._create_column("loop_mrid", "TEXT", Nullable.NULL)

    @property
    def name(self) -> str:
        return "circuits"

    @property
    def non_unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().non_unique_index_columns
        yield [self.loop_mrid]
