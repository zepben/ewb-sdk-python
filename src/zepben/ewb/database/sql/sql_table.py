#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

__all__ = ["SqlTable"]

from abc import abstractmethod, ABCMeta
from operator import attrgetter
from typing import List, Optional, Type, Any, Generator

from zepben.ewb.database.sql.column import Column, Nullable


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
        if self._prepared_insert_sql is None:
            self._prepared_insert_sql = (f"INSERT INTO {self.name} ({', '.join([c.name for c in self.column_set])}) "
                                         f"VALUES ({', '.join(['?' for _ in self.column_set])})")
        return self._prepared_insert_sql

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
        if self._select_sql is None:
            self._select_sql = f"SELECT {', '.join([c.name for c in self.column_set])} FROM {self.name}"
        return self._select_sql

    @property
    def prepared_update_sql(self):
        """
        The SQL statement that should be used with a `PreparedStatement` to update entries into the table.
        """
        if self._prepared_update_sql is None:
            self._prepared_update_sql = f"UPDATE {self.name} SET {', '.join([f'{c.name} = ?' for c in self.column_set])}"
        return self._prepared_update_sql

    @property
    def unique_index_columns(self) -> Generator[List[Column], None, None]:
        """
        A list of column groups that require a unique index in the database
        """
        yield from []

    @property
    def non_unique_index_columns(self) -> Generator[List[Column], None, None]:
        """
        A list of column groups that require a non-unique index in the database
        """
        yield from []

    @property
    def column_set(self) -> List[Column]:
        if self._column_set is None:
            self._column_set = list(self._build_column_set(self.__class__, self))
        return self._column_set

    @staticmethod
    def _build_column_set(clazz: Type[Any], instance: SqlTable) -> Generator[Column, None, None]:
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
            raise ValueError("You have duplicate column names, go fix that.")

        yield from sorted(cols, key=attrgetter('query_index'))

    def _create_column(self, name: str, type_: str, nullable: Nullable = Nullable.NONE) -> Column:
        self.column_index += 1
        # noinspection PyArgumentList
        return Column(self.column_index, name, type_, nullable)
