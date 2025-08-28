#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["TableIdentifiedObjects"]

from abc import ABC
from typing import List, Generator

from zepben.ewb.database.sql.column import Column, Nullable
from zepben.ewb.database.sqlite.tables.sqlite_table import SqliteTable


class TableIdentifiedObjects(SqliteTable, ABC):

    def __init__(self):
        self.mrid: Column = self._create_column("mrid", "TEXT", Nullable.NOT_NULL)
        self.name_: Column = self._create_column("name", "TEXT", Nullable.NULL)
        self.description: Column = self._create_column("description", "TEXT", Nullable.NULL)
        self.num_diagram_objects: Column = self._create_column("num_diagram_objects", "INTEGER", Nullable.NULL)

    @property
    def unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield [self.mrid]

    @property
    def non_unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield [self.name_]
