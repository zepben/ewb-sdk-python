#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import logging
from sqlite3 import Cursor
from typing import Callable, Type, TypeVar

from zepben.evolve import DatabaseTables, BaseCIMReader, TableNameTypes, TableNames, SqliteTable, ResultSet

logger = logging.getLogger(__name__)
__all__ = ["BaseServiceReader"]

TSqliteTable = TypeVar("TSqliteTable", bound=SqliteTable)


class BaseServiceReader(object):
    """
    Base class for reading a service from the database.
    """

    _get_cursor: Callable[[], Cursor]
    _database_tables = DatabaseTables()

    def __init__(self, get_cursor: Callable[[], Cursor]):
        """
        :param get_cursor: Provider of cursors for the connection.
        """
        self._get_cursor = get_cursor

    def load_name_types(self, reader: BaseCIMReader) -> bool:
        status = True
        status = status and self._load_each(TableNameTypes, "name type", reader.load_name_type)

        return status

    def load_names(self, reader: BaseCIMReader) -> bool:
        status = True
        status = status and self._load_each(TableNames, "name", reader.load_name)

        return status

    def _load_each(
        self,
        table_type: Type[TSqliteTable],
        description: str,
        process_row: Callable[[TSqliteTable, ResultSet, Callable[[str], str]], bool]
    ) -> bool:
        def process_rows(db_table: SqliteTable, results: ResultSet):
            last_identifier = None

            def set_last_identifier(identifier: str) -> str:
                nonlocal last_identifier
                last_identifier = identifier
                return identifier

            try:
                count = 0
                while results.next():
                    if process_row(db_table, results, set_last_identifier):
                        count = count + 1

                return count
            except Exception as e:
                logger.error(f"Failed to load '{last_identifier}' from '{db_table.name()}': {str(e)}")
                raise e

        return self._load_table(table_type, description, process_rows)

    def _load_table(
        self,
        table_type: Type[TSqliteTable],
        description: str,
        process_rows: Callable[[TSqliteTable, ResultSet], int]
    ) -> bool:
        logger.info(f"Loading {description}...")

        table = self._database_tables.get_table(table_type)
        try:
            cur = self._get_cursor()
            cur.execute(table.select_sql())
            count = process_rows(table, ResultSet(cur.fetchall()))

            logger.info(f"Successfully loaded {count} {description}.")
            return True
        except Exception as e:
            logger.error(f"Failed to read the {description} from '{table.name()}': {str(e)}", exc_info=e)
            return False
