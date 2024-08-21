#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
__all__ = ["BaseCollectionReader"]

import logging
from abc import ABC, abstractmethod
from contextlib import closing
from sqlite3 import Connection
from typing import Callable, Type, Optional

from zepben.evolve.database.sqlite.common.base_database_tables import BaseDatabaseTables, TSqliteTable
from zepben.evolve.database.sqlite.common.reader_exceptions import MRIDLookupException, DuplicateMRIDException
from zepben.evolve.database.sqlite.extensions.prepared_statement import SqlException
from zepben.evolve.database.sqlite.extensions.result_set import ResultSet


class BaseCollectionReader(ABC):
    """
    A base class for reading collections of object collections from a database.
    """

    def __init__(self, tables: BaseDatabaseTables, connection: Connection):
        super().__init__()
        self._logger: logging.Logger = logging.getLogger(self.__class__.__name__)
        """
        The logger to use for this collection reader.
        """

        self.base_database_tables: BaseDatabaseTables = tables
        """
        The tables that are available in the database.
        """

        self._connection: Connection = connection
        """
        The connection to the database to read.
        """

    @abstractmethod
    def load(self) -> bool:
        """
        Load all the objects for the available collections.

        :return: True if the load was successful, otherwise False.
        """
        pass

    def _load_each(self, type_: Type[TSqliteTable], process_row: Callable[[TSqliteTable, ResultSet, Callable[[str], str]], bool]) -> bool:
        """
        Load each row of a table.

        :param type_: The `SqliteTable` to read the objects from.
        :param process_row: A callback for processing each row in the table. The callback will be provided with the table, the results for the row and a
          callback to set the identifier for the row, which returns the same value, so it can be used fluently.
        """
        table = self.base_database_tables.get_table(type_)

        def process_rows(results: ResultSet):
            last_identifier: Optional[str] = None

            def set_identifier(identifier: str) -> str:
                nonlocal last_identifier
                last_identifier = identifier
                return identifier

            try:
                count = 0
                while results.next():
                    if process_row(table, results, set_identifier):
                        count = count + 1

                return count
            except SqlException as e:
                self._logger.error(f"Failed to load '{last_identifier}' from '{table.name}': {e}")
                raise e

        return self._load_all(table, process_rows)

    def _load_all(self, table: TSqliteTable, process_rows: Callable[[ResultSet], int]) -> bool:
        """
        You really shouldn't need to use this function directly, use `load_each` instead.
        """
        self._logger.info(f"Loading {table.describe()}...")

        try:
            with closing(self._connection.cursor()) as cur:
                cur.execute(table.select_sql)
                count = process_rows(ResultSet(cur.fetchall()))
            self._logger.info(f"Successfully loaded {count} {table.describe()}.")
            return True
        except (SqlException, ValueError, MRIDLookupException, DuplicateMRIDException) as ex:
            self._logger.exception(f"Failed to read the {table.describe()} from '{table.name}': {ex}")
            return False
