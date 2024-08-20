#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List, Generator

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_identified_objects import TableIdentifiedObjects

__all__ = ["TableTransformerStarImpedances"]


class TableTransformerStarImpedances(TableIdentifiedObjects):

    def __init__(self):
        super().__init__()
        # Note r, r0, x, x0 use nullable number types.
        self.r: Column = self._create_column("R", "NUMBER", Nullable.NULL)
        self.r0: Column = self._create_column("R0", "NUMBER", Nullable.NULL)
        self.x: Column = self._create_column("X", "NUMBER", Nullable.NULL)
        self.x0: Column = self._create_column("X0", "NUMBER", Nullable.NULL)
        self.transformer_end_info_mrid: Column = self._create_column("transformer_end_info_mrid", "TEXT", Nullable.NULL)

    @property
    def name(self) -> str:
        return "transformer_star_impedances"

    @property
    def unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().unique_index_columns
        yield [self.transformer_end_info_mrid]
