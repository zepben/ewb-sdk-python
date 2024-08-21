#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from typing import List

from pytest import raises

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.sqlite_table import SqliteTable


def test_create_column_set():
    x = WorkingTables()
    cs = x.column_set

    assert len(cs) == 2
    assert cs[0] == x.test_column
    assert cs[1] == x.test_column_2


def test_ddl():
    x = WorkingTables()
    assert x.create_table_sql == "CREATE TABLE test_table (test_column TEXT NOT NULL, test_column_2 TEXT NULL)"
    assert x.select_sql == "SELECT test_column, test_column_2 FROM test_table"
    assert x.prepared_insert_sql == "INSERT INTO test_table (test_column, test_column_2) VALUES (?, ?)"
    assert x.prepared_update_sql == "UPDATE test_table SET test_column = ?, test_column_2 = ?"
    assert x.create_indexes_sql == [f"CREATE UNIQUE INDEX test_table_test_column ON test_table (test_column)",
                                    f"CREATE INDEX test_table_test_column_2 ON test_table (test_column_2)"]


def test_create_column_set_raises_on_invalid_column_name():
    x = TableWithDuplicateColumnName()
    with raises(ValueError, match="You have a duplicate column names, go fix that."):
        _ = x.column_set


def test_create_column_set_raises_on_invalid_column_index():
    x = TableWithDuplicateColumnIndex()
    with raises(ValueError,
                match="Field test_column_2 in SQL Table class TableWithDuplicateColumnIndex is using an invalid column index. "
                      "Did you forget to increment column_index, or did you skip one?"):
        _ = x.column_set


def test_create_column_set_raises_on_missing_column_index():
    x = TableWithMissingColumnIndex()
    with raises(ValueError,
                match="Field test_column_2 in SQL Table class TableWithMissingColumnIndex is using an invalid column index. "
                      "Did you forget to increment column_index, or did you skip one?"):
        _ = x.column_set


class WorkingTables(SqliteTable):
    # Confirm the table ignores non-column fields, public and private.
    __test__ = False
    _ignored_field_1: str = "field"
    ignored_field_2: str = "field"

    def __init__(self):
        self.test_column: Column = self._create_column("test_column", "TEXT", Nullable.NOT_NULL)
        self.test_column_2: Column = self._create_column("test_column_2", "TEXT", Nullable.NULL)

    @property
    def name(self) -> str:
        return "test_table"

    @property
    def unique_index_columns(self) -> List[List[Column]]:
        return [[self.test_column]]

    @property
    def non_unique_index_columns(self) -> List[List[Column]]:
        return [[self.test_column_2]]


class TableWithDuplicateColumnName(SqliteTable):

    def __init__(self):
        """simulate copy/paste error"""
        self.test_column: Column = self._create_column("test_column", "TEXT", Nullable.NOT_NULL)
        self.test_column_2: Column = self._create_column("test_column", "TEXT", Nullable.NOT_NULL)

    @property
    def name(self) -> str:
        return "test_table"


class TableWithDuplicateColumnIndex(SqliteTable):

    def __init__(self):
        """simulate not using helper for creating columns and messing up the indexes"""
        # noinspection PyArgumentList
        self.test_column = Column(1, "test_column", "TEXT", Nullable.NOT_NULL)
        # noinspection PyArgumentList
        self.test_column_2 = Column(1, "test_column_2", "TEXT", Nullable.NULL)

    @property
    def name(self) -> str:
        return "test_table"


class TableWithMissingColumnIndex(SqliteTable):

    def __init__(self):
        """simulate not using helper for creating columns and messing up the indexes"""
        # noinspection PyArgumentList
        self.test_column = Column(1, "test_column", "TEXT", Nullable.NOT_NULL)
        # noinspection PyArgumentList
        self.test_column_2 = Column(3, "test_column_2", "TEXT", Nullable.NULL)

    @property
    def name(self) -> str:
        return "test_table"
