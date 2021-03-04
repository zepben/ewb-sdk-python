#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations
from typing import Type

from pytest import raises

from zepben.evolve import Column, Nullable
from zepben.evolve.database.sqlite.tables.sqlite_table import SqliteTable


class TestTable(SqliteTable):

    test_column: Column = None
    test_column_2: Column = None
    _ignored_column: Column = None
    _ignored_field: str = "field"

    def __init__(self):
        self.column_index += 1
        self.test_column = Column(self.column_index, "test_column", "TEXT", Nullable.NOT_NULL)
        self.column_index += 1
        self._ignored_column = Column(self.column_index, "test_column", "TEXT", Nullable.NOT_NULL)
        self.column_index += 1
        self.test_column_2 = Column(self.column_index, "test_column_2", "TEXT", Nullable.NULL)

    @property
    def table_class(self) -> Type[TestTable]:
        return self.__class__

    @property
    def table_class_instance(self) -> TestTable:
        return self

    def name(self) -> str:
        return "test table"


class TestTable2(SqliteTable):

    test_column: Column = None
    test_column_2: Column = None

    def __init__(self):
        self.column_index += 1
        self.test_column = Column(self.column_index, "test_column", "TEXT", Nullable.NOT_NULL)
        self.test_column_2 = Column(self.column_index, "test_column_2", "TEXT", Nullable.NULL)

    @property
    def table_class(self) -> Type[TestTable2]:
        return self.__class__

    @property
    def table_class_instance(self) -> TestTable2:
        return self

    def name(self) -> str:
        return "test table"


def test_create_column_set():
    x = TestTable()
    cs = x.column_set()
    assert cs[0] == x.test_column
    assert cs[1] == x.test_column_2
    assert x._ignored_column not in cs
    assert x._ignored_field not in cs
    assert x.table_class not in cs
    assert x.name not in cs


def test_create_column_set_raises_on_invalid_index():
    x = TestTable2()
    with raises(ValueError, match="Field test_column_2 in SQL Table class TestTable2 is using an index that has already been used. Did you forget to increment column_index?"):
        cs = x.column_set()


class TestTable3(SqliteTable):

    test_column: Column = None
    test_column_2: Column = None

    def __init__(self):
        self.column_index += 1
        self.test_column = Column(self.column_index, "test_column", "TEXT", Nullable.NOT_NULL)
        self.column_index += 1
        self.test_column_2 = Column(self.column_index, "test_column_2", "TEXT", Nullable.NULL)

    @property
    def test_prop(self):
        raise Exception("test")

    @property
    def table_class(self) -> Type[TestTable3]:
        return self.__class__

    @property
    def table_class_instance(self) -> TestTable3:
        return self

    def name(self) -> str:
        return "test table"


def test_create_column_set_raises_on_exception():
    x = TestTable3()
    with raises(ValueError, match="Unable to retrieve field test_prop. It will be missing from the database. Error was: test"):
        cs = x.column_set()
