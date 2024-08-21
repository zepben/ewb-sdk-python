#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
__all__ = ["TSqliteTable", "BaseDatabaseTables"]

from abc import ABC
from sqlite3 import Connection, Cursor, ProgrammingError
from typing import Dict, TypeVar, Type, Generator, Callable, Optional

from zepben.evolve.database.sqlite.extensions.prepared_statement import PreparedStatement
from zepben.evolve.database.sqlite.tables.exceptions import MissingTableConfigException
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_name_types import *
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_names import *
from zepben.evolve.database.sqlite.tables.sqlite_table import *
from zepben.evolve.database.sqlite.tables.table_metadata_data_sources import TableMetadataDataSources
from zepben.evolve.database.sqlite.tables.table_version import TableVersion

TSqliteTable = TypeVar("TSqliteTable", bound=SqliteTable)


class BaseDatabaseTables(ABC):
    """
    The base collection of tables for all our databases.
    """

    def __init__(self):
        super().__init__()
        self._tables: Optional[Dict[Type[TSqliteTable], SqliteTable]] = None
        self._insert_statements: Optional[Dict[Type[TSqliteTable], PreparedStatement]] = None
        self._insert_cursor: Optional[Cursor] = None

    @property
    def tables(self) -> Generator[SqliteTable, None, None]:
        """
        The tables that are available in this database, keyed on the table class. You should use `get_table` to access individual tables.
        """
        self._ensure_tables()
        for t in self._tables.values():
            yield t

    @property
    def insert_statements(self) -> Generator[PreparedStatement, None, None]:
        """
        A collection of `PreparedStatement` for each table. You should use `get_insert` to access individual inserts.
        """
        if self._insert_statements is not None:
            for s in self._insert_statements.values():
                yield s

    @property
    def _included_tables(self) -> Generator[SqliteTable, None, None]:
        """
        A sequence of `SqliteTable` indicating which tables are included in this database, which will be consumed to build the `tables` collection.

        NOTE: You should always append your tables to `super()._included_tables` when overriding.
        """
        yield TableMetadataDataSources()
        yield TableVersion()
        yield TableNameTypes()
        yield TableNames()

    def get_table(self, type_: Type[TSqliteTable]) -> TSqliteTable:
        """
        Helper function for getting the table of the specified type.

        :param type_: The type of table to get.
        :return: The requested table if it belongs to this database.
        :raises MissingTableConfigException: If the requested table doesn't belong to this database.
        """
        self._ensure_tables()
        try:
            return self._tables[type_]
        except KeyError:
            raise MissingTableConfigException(f"INTERNAL ERROR: No table has been registered for {type_}. You might want to consider fixing that.")

    def get_insert(self, type_: Type[TSqliteTable]) -> PreparedStatement:
        """
        Helper function for getting the insert statement for the specified table.

        :param type_: The type of table to get.
        :return: The insert statement for the requested table if it belongs to this database.
        :raises MissingTableConfigException: If the requested table doesn't belong to this database.
        """
        try:
            return self._insert_statements[type_]
        except KeyError:
            raise MissingTableConfigException(f"INTERNAL ERROR: No prepared statement has been registered for {type_}. You might want to consider fixing that.")
        except TypeError:
            raise MissingTableConfigException("INTERNAL ERROR: Statements have not been prepared. You must call `prepare_insert_statements` first.")

    def for_each_table(self, action: Callable[[SqliteTable], None]):
        """
        Call the `action` on each table.

        :param action: A callback invoked on each table.
        """
        for t in self.tables:
            action(t)

    def prepare_insert_statements(self, connection: Connection):
        """
        Create a `PreparedStatement` for inserting into each table.

        :param connection: The `Connection` to prepare the statements on.
        """
        self._close_insert_statements()

        # Make sure the underlying collection has been populated.
        self._ensure_tables()

        self._insert_cursor = connection.cursor()
        self._insert_statements = dict()
        for t, table in self._tables.items():
            self._insert_statements[t] = PreparedStatement(table.prepared_insert_sql, self._insert_cursor)

    def close(self):
        self._close_insert_statements()

    def _close_insert_statements(self):
        try:
            if self._insert_cursor:
                self._insert_cursor.close()
            self._insert_cursor = None
        except ProgrammingError:
            # Can be thrown when the database is closed
            pass

        if self.insert_statements:
            for s in self.insert_statements:
                s.close()
        self._insert_statements = None

    def _ensure_tables(self):
        if not self._tables:
            self._tables = {type(it): it for it in self._included_tables}
