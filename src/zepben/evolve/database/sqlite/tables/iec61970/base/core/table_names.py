#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List, Generator

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.sqlite_table import SqliteTable


__all__ = ["TableNames"]


class TableNames(SqliteTable):

    def __init__(self):
        super().__init__()
        self.name_: Column = self._create_column("name", "TEXT", Nullable.NOT_NULL)
        self.identified_object_mrid: Column = self._create_column("identified_object_mrid", "TEXT", Nullable.NOT_NULL)
        self.name_type_name: Column = self._create_column("name_type_name", "TEXT", Nullable.NOT_NULL)

    @property
    def name(self) -> str:
        return "names"

    @property
    def unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().unique_index_columns
        yield [self.identified_object_mrid, self.name_type_name, self.name_]

    @property
    def non_unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().non_unique_index_columns
        yield [self.identified_object_mrid]
        yield [self.name_]
        yield [self.name_type_name]
