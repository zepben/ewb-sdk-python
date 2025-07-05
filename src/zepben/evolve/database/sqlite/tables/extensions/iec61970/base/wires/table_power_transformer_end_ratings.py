#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List, Generator

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.sqlite_table import SqliteTable


__all__ = ["TablePowerTransformerEndRatings"]


class TablePowerTransformerEndRatings(SqliteTable):

    def __init__(self):
        super().__init__()
        self.power_transformer_end_mrid: Column = self._create_column("power_transformer_end_mrid", "TEXT", Nullable.NOT_NULL)
        self.cooling_type: Column = self._create_column("cooling_type", "TEXT", Nullable.NOT_NULL)
        self.rated_s: Column = self._create_column("rated_s", "INTEGER", Nullable.NOT_NULL)

    @property
    def name(self) -> str:
        return "power_transformer_end_ratings"

    @property
    def unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().unique_index_columns
        yield [self.power_transformer_end_mrid, self.cooling_type]

    @property
    def non_unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().non_unique_index_columns
        yield [self.power_transformer_end_mrid]
