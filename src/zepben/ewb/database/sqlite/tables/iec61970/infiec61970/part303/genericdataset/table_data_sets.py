#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["TableDataSets"]

from abc import ABC

from zepben.ewb.database.sql.column import Column, Nullable, Type
from zepben.ewb.database.sqlite.tables.sqlite_table import SqliteTable


class TableDataSets(SqliteTable, ABC):
    """
    A class representing the `DataSet` columns required for the database table.
    """

    def __init__(self):
        super().__init__()
        self.mrid: Column = self._create_column("mrid", Type.STRING, Nullable.NOT_NULL)
        self.name_: Column = self._create_column("name", Type.STRING, Nullable.NULL)
        self.description: Column = self._create_column("description", Type.STRING, Nullable.NULL)

    @property
    def unique_index_columns(self):
        yield [self.mrid]

    @property
    def non_unique_index_columns(self):
        yield [self.name_]
