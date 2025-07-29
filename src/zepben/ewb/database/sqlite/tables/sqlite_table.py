#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["SqliteTable"]

from abc import ABC
from typing import List, Generator

from zepben.ewb.database.sql.column import Column
from zepben.ewb.database.sql.sql_table import SqlTable


class SqliteTable(SqlTable, ABC):
    """
    Represents a table in an Sqlite Database.
    """

    @property
    def create_table_sql(self):
        if self._create_table_sql is None:
            self._create_table_sql = self._build_create_table_sql()
        return self._create_table_sql

    @property
    def create_indexes_sql(self):
        if self._create_indexes_sql is None:
            self._create_indexes_sql = list(self._build_indexes_sql())
        return self._create_indexes_sql

    def _build_create_table_sql(self) -> str:
        return f"CREATE TABLE {self.name} ({', '.join(str(c) for c in self.column_set)})"

    def _build_indexes_sql(self) -> Generator[str, None, None]:
        yield from (self._build_index_sql(index_col, True) for index_col in self.unique_index_columns)
        yield from (self._build_index_sql(index_col, False) for index_col in self.non_unique_index_columns)

    def _build_index_sql(self, index_col: List[Column], is_unique: bool) -> str:
        index_col_names = [c.name for c in index_col]
        return (f"CREATE {'UNIQUE ' if is_unique else ''}INDEX "
                f"{self.name}_{'_'.join(index_col_names)}"  # id string
                f" ON {self.name} ({', '.join(index_col_names)})")  # col string
