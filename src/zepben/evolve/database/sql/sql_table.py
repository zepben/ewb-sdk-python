#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from abc import abstractmethod, ABC, ABCMeta
from typing import List, Optional, Type, Any, Generator

from zepben.evolve.database.sql.column import Column, Nullable

__all__ = ["SqlTable"]


class SqlTable(metaclass=ABCMeta):
    """
    Represents a table in an SQL Database.

    By default, this class doesn't support creating schema creation statements, allowing support for database with external schema management.
    """

    column_index: int = 0
    """Used to specify index of the column in the table during initialisation. Always increment BEFORE creating a Column. Indices start from 1."""

    _column_set: Optional[List[Column]] = None
    _create_table_sql: Optional[str] = None
    _prepared_insert_sql: Optional[str] = None
    _prepared_update_sql: Optional[str] = None
    _create_indexes_sql: Optional[List[str]] = None
    _select_sql: Optional[str] = None

    @property
    @abstractmethod
    def name(self) -> str:
        """
        The name of the table in the actual database.
        """
        pass

    #
    # NOTE: This function is called `description` in teh JVM SDK, but in the python SDK this
    #       conflicts with the `description` column of `TableIdentifiedObjects`.
    #
    def describe(self) -> str:
        """
        Readable description of the contents of the table for adding to logs.
        """
        return self.name.replace("_", " ")

    @property
    @abstractmethod
    def create_table_sql(self):
        """
        The SQL statement that should be executed to create the table in the database.
        """
        raise NotImplemented

    @property
    def prepared_insert_sql(self):
        """
        The SQL statement that should be used with a `PreparedStatement` to insert entries into the table.
        """
        return self._prepared_insert_sql if self._prepared_insert_sql else self._build_prepared_insert_sql()

    @property
    @abstractmethod
    def create_indexes_sql(self):
        """
        The SQL statement that should be executed to create the indexes for the table in the database. Should be executed after all
        entries are inserted into the table.
        """
        raise NotImplemented

    @property
    def select_sql(self):
        """
        The SQL statement that should be used to read the entries from the table in the database.
        """
        return self._select_sql if self._select_sql else self._build_select_sql()

    @property
    def prepared_update_sql(self):
        """
        The SQL statement that should be used with a `PreparedStatement` to update entries into the table.
        """
        return self._prepared_update_sql if self._prepared_update_sql else self._build_prepared_update_sql()

    @property
    def unique_index_columns(self) -> Generator[List[Column], None, None]:
        """
        A list of column groups that require a unique index in the database
        """
        # To make this a generator we need to `yield`, but we have nothing to yield by default, so trick it by yielding from an empty for-loop.
        for it in []:
            yield it

    @property
    def non_unique_index_columns(self) -> Generator[List[Column], None, None]:
        """
        A list of column groups that require a non-unique index in the database
        """
        # To make this a generator we need to `yield`, but we have nothing to yield by default, so trick it by yielding from an empty for-loop.
        for it in []:
            yield it

    @property
    def column_set(self) -> List[Column]:
        return self._column_set if self._column_set else self._build_column_set(self.__class__, self)

    def _build_column_set(self, clazz: Type[Any], instance: SqlTable) -> List[Column]:
        """
        Builds the list of columns for use in DDL statements for this table.

        :param clazz: The class of this table.
        :param instance:
        """
        cols = list()
        for field, x in instance.__dict__.items():
            if isinstance(x, Column):
                if x.query_index != len(cols) + 1:
                    raise ValueError(
                        f"Field {field} in SQL Table class {clazz.__name__} is using an invalid column index. "
                        f"Did you forget to increment column_index, or did you skip one?"
                    )
                cols.append(x)

        if len(set([c.name for c in cols])) != len(cols):
            raise ValueError("You have a duplicate column names, go fix that.")

        self._column_set = sorted(cols, key=lambda it: it.query_index)
        return self._column_set

    def _build_prepared_insert_sql(self) -> str:
        self._prepared_insert_sql = f"INSERT INTO {self.name} ({', '.join([c.name for c in self.column_set])}) " \
                                    f"VALUES ({', '.join(['?' for _ in self.column_set])})"
        return self._prepared_insert_sql

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

    def _build_select_sql(self) -> str:
        self._select_sql = f"SELECT {', '.join([c.name for c in self.column_set])} FROM {self.name}"
        return self._select_sql

    def _build_prepared_update_sql(self) -> str:
        self._prepared_update_sql = f"UPDATE {self.name} SET {', '.join([f'{c.name} = ?' for c in self.column_set])}"
        return self._prepared_update_sql

    def _create_column(self, name: str, type_: str, nullable: Nullable = Nullable.NONE) -> Column:
        self.column_index += 1
        # noinspection PyArgumentList
        return Column(self.column_index, name, type_, nullable)
