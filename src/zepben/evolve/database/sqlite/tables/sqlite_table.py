#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

import inspect
from abc import abstractmethod
from typing import List, Optional, Type, TypeVar, Any

from dataclassy import dataclass

from zepben.evolve.database.sqlite.tables.column import Column, Nullable

__all__ = ["SqliteTable"]


@dataclass(slots=True)
class SqliteTable(object):
    """
    Represents a table in an Sqlite Database. This class should be extended and initialised to build the DDL for a Table.
    Methods that need to be overridden are those marked @abstractmethod.
    Methods that can be optionally overridden are unique_index_columns() and non_unique_index_columns().
    Columns must be assigned in __init__ and column_index must be incremented for each Column created.
    See existing implementations such as TableVersion for examples.
    """

    column_index: int = 0
    """Used to specify index of the column in the table during initialisation. Always increment BEFORE creating a Column. Indices start from 1."""

    _column_set: Optional[List[Column]] = None
    _create_table_sql: Optional[str] = None
    _prepared_insert_sql: Optional[str] = None
    _prepared_update_sql: Optional[str] = None
    _create_indexes_sql: Optional[List[str]] = None
    _select_sql: Optional[str] = None

    @abstractmethod
    def name(self) -> str:
        pass

    def unique_index_columns(self) -> List[List[Column]]:
        return []

    def non_unique_index_columns(self) -> List[List[Column]]:
        return []

    def column_set(self) -> List[Column]:
        return self._column_set if self._column_set else self._build_column_set(self.__class__, self)

    def create_table_sql(self):
        return self._create_table_sql if self._create_table_sql else self._build_create_table_sql()

    def select_sql(self):
        return self._select_sql if self._select_sql else self._build_select_sql()

    def prepared_insert_sql(self):
        return self._prepared_insert_sql if self._prepared_insert_sql else self._build_prepared_insert_sql()

    def prepared_update_sql(self):
        return self._prepared_update_sql if self._prepared_update_sql else self._build_prepared_update_sql()

    def create_indexes_sql(self):
        return self._create_indexes_sql if self._create_indexes_sql else self._build_indexes_sql()

    def _build_column_set(self, clazz: Type[Any], instance: Any) -> List[Column]:
        """
        Builds the list of columns for use in DDL statements for this table.

        :param clazz: The class of this table.
        :param instance:
        :return:
        """
        cols = list()

        attributes = inspect.getmembers(clazz, lambda it: not inspect.isroutine(it))
        declared_fields = [a for a in attributes if not a[0].startswith('_')]
        for field, _ in declared_fields:
            try:
                x = getattr(instance, field)
                if isinstance(x, Column):
                    for c in cols:
                        if x.query_index == c.query_index:
                            raise ValueError(
                                f"Field {field} in SQL Table class {clazz.__name__} is using an index that has already been used. "
                                f"Did you forget to increment column_index?"
                            )
                    cols.append(x)
            except Exception as e:
                raise ValueError(f"Unable to retrieve field {field}. It will be missing from the database. Error was: {str(e)}")

        self._column_set = sorted(cols, key=lambda it: it.query_index)
        return self._column_set

    def _build_create_table_sql(self) -> str:
        self._create_table_sql = f"CREATE TABLE {self.name()} ({', '.join([str(c) for c in self.column_set()])})"
        return self._create_table_sql

    def _build_select_sql(self) -> str:
        self._select_sql = f"SELECT {', '.join([c.name for c in self.column_set()])} FROM {self.name()}"
        return self._select_sql

    def _build_prepared_insert_sql(self) -> str:
        self._prepared_insert_sql = f"INSERT INTO {self.name()} ({', '.join([c.name for c in self.column_set()])}) " \
                                    f"VALUES ({', '.join(['?' for _ in self.column_set()])})"
        return self._prepared_insert_sql

    def _build_prepared_update_sql(self) -> str:
        self._prepared_update_sql = f"UPDATE {self.name()} SET {', '.join([f'{c.name} = ?' for c in self.column_set()])}"
        return self._prepared_update_sql

    def _build_indexes_sql(self) -> List[str]:
        statements = []
        for index_col in self.unique_index_columns():
            statements.append(self._build_index_sql(index_col, True))
        for index_col in self.non_unique_index_columns():
            statements.append(self._build_index_sql(index_col, False))
        self._create_indexes_sql = statements
        return self._create_indexes_sql

    def _build_index_sql(self, index_col: List[Column], is_unique: bool):
        id_string = f"{self.name()}_{'_'.join(map(lambda c: c.name, index_col))}"
        col_string = ', '.join(map(lambda c: c.name, index_col))
        return f"CREATE {'UNIQUE ' if is_unique else ''}INDEX {id_string} ON {self.name()} ({col_string})"

    def _create_column(self,
                       name: str,
                       type_: str,
                       nullable: Nullable = Nullable.NONE
                       ) -> Column:
        self.column_index += 1
        # noinspection PyArgumentList
        return Column(self.column_index, name, type_, nullable)


T = TypeVar("T", bound=SqliteTable)
