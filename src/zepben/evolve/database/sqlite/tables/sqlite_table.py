#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from abc import ABC
from typing import List, Optional

from zepben.evolve.database.sql.column import Column

__all__ = ["SqliteTable"]

from zepben.evolve.database.sql.sql_table import SqlTable


class SqliteTable(SqlTable, ABC):
    """
    Represents a table in an Sqlite Database.
    """

    _column_set: Optional[List[Column]] = None
    _create_table_sql: Optional[str] = None
    _prepared_insert_sql: Optional[str] = None
    _prepared_update_sql: Optional[str] = None
    _create_indexes_sql: Optional[List[str]] = None
    _select_sql: Optional[str] = None

    @property
    def create_table_sql(self):
        return self._create_table_sql if self._create_table_sql else self._build_create_table_sql()

    @property
    def create_indexes_sql(self):
        return self._create_indexes_sql if self._create_indexes_sql else self._build_indexes_sql()

    def _build_create_table_sql(self) -> str:
        self._create_table_sql = f"CREATE TABLE {self.name} ({', '.join([str(c) for c in self.column_set])})"
        return self._create_table_sql

    def _build_indexes_sql(self) -> List[str]:
        statements = []
        for index_col in self.unique_index_columns:
            statements.append(self._build_index_sql(index_col, True))
        for index_col in self.non_unique_index_columns:
            statements.append(self._build_index_sql(index_col, False))
        self._create_indexes_sql = statements
        return self._create_indexes_sql

    def _build_index_sql(self, index_col: List[Column], is_unique: bool):
        id_string = f"{self.name}_{'_'.join(map(lambda c: c.name, index_col))}"
        col_string = ', '.join(map(lambda c: c.name, index_col))
        return f"CREATE {'UNIQUE ' if is_unique else ''}INDEX {id_string} ON {self.name} ({col_string})"
