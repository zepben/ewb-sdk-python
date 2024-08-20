#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
__all__ = ["BaseDatabaseWriter"]

import logging
import os
from abc import ABC
from contextlib import closing
from pathlib import Path
from sqlite3 import Connection, Cursor, OperationalError
from typing import Callable, Union

from zepben.evolve.database.sqlite.common.base_database_tables import BaseDatabaseTables
from zepben.evolve.database.sqlite.common.base_service_writer import BaseServiceWriter
from zepben.evolve.database.sqlite.common.metadata_collection_writer import MetadataCollectionWriter
from zepben.evolve.database.sqlite.extensions.prepared_statement import SqlException, PreparedStatement
from zepben.evolve.database.sqlite.tables.exceptions import MissingTableConfigException
from zepben.evolve.database.sqlite.tables.sqlite_table import SqliteTable
from zepben.evolve.database.sqlite.tables.table_version import TableVersion


class BaseDatabaseWriter(ABC):
    """
    A base class for writing objects to one of our databases.
    """

    def __init__(
        self,
        database_file: Union[Path, str],
        database_tables: BaseDatabaseTables,
        create_metadata_writer: Callable[[], MetadataCollectionWriter],
        create_service_writer: Callable[[], BaseServiceWriter],
        get_connection: Callable[[str], Connection]
    ):
        super().__init__()
        self._logger: logging.Logger = logging.getLogger(self.__class__.__name__)
        """
        The logger to use for this database writer.
        """

        self._database_file: str = str(database_file)
        """
        The filename of the database to write.
        """

        self._database_tables: BaseDatabaseTables = database_tables
        """
        The tables to create in the database.
        """

        self._create_metadata_writer: Callable[[], MetadataCollectionWriter] = create_metadata_writer
        """
        Create a [MetadataCollectionWriter] that uses the provided [Connection].
        """

        self._create_service_writer: Callable[[], BaseServiceWriter] = create_service_writer
        """
        Create a [BaseServiceWriter] that uses the provided [Connection].
        """

        self._get_connection: Callable[[str], Connection] = get_connection
        """
        Provider of the connection to the specified database.
        """

        self._save_connection: Connection
        self._has_been_used: bool = False

    def save(self) -> bool:
        """
        Save the database using the [MetadataCollectionWriter] and [BaseServiceWriter].

        @return True if the database was successfully saved, otherwise False.
        """
        if self._has_been_used:
            self._logger.error(f"You can only use the database writer once.")
            return False
        self._has_been_used = True

        if not self._pre_save():
            self._close_connection()
            return False

        status: bool
        try:
            status = all([
                self._create_metadata_writer().save(),
                self._create_service_writer().save()
            ])
        except MissingTableConfigException as e:
            self._logger.exception(f"Unable to save database: {e}")
            status = False

        return all([status, self._post_save()])

    def _pre_save(self) -> bool:
        return (self._remove_existing()
                and self._connect()
                and self._create()
                and self._prepare_insert_statements())

    def _remove_existing(self) -> bool:
        try:
            if os.path.isfile(self._database_file):
                os.remove(self._database_file)
            return True
        except Exception as e:
            self._logger.exception(f"Unable to save database, failed to remove previous instance: {e}")
            return False

    def _connect(self) -> bool:
        try:
            self._save_connection = self._get_connection(self._database_file)

            cur: Cursor
            with closing(self._save_connection.cursor()) as cur:
                cur.execute("PRAGMA journal_mode = OFF")
                cur.execute("PRAGMA synchronous = OFF")

            self._save_connection.isolation_level = None  # autocommit off

            return True
        except (SqlException, OperationalError) as e:
            self._logger.exception(f"Failed to connect to the database for saving: {e}")
            self._close_connection()
            return False

    def _prepare_insert_statements(self) -> bool:
        try:
            self._database_tables.prepare_insert_statements(self._save_connection)
            return True
        except SqlException as e:
            self._logger.exception(f"Failed to prepare insert statements: {e}")
            self._close_connection()
            return False

    def _create(self) -> bool:
        try:
            version_table = self._database_tables.get_table(TableVersion)
            self._logger.info(f"Creating database schema v{version_table.SUPPORTED_VERSION}...")

            cur: Cursor
            with closing(self._save_connection.cursor()) as cur:
                def create_table(it: SqliteTable):
                    cur.execute(it.create_table_sql)

                self._database_tables.for_each_table(create_table)

                # Add the version number to the database.
                insert = PreparedStatement(version_table.prepared_insert_sql, cur)
                insert.add_value(version_table.version.query_index, version_table.SUPPORTED_VERSION)
                insert.execute()

                self._save_connection.commit()
                self._logger.info("Schema created.")

            return True
        except SqlException as e:
            self._logger.exception(f"Failed to create database schema: {e}")
            return False

    def _close_connection(self):
        try:
            if self._save_connection is not None:
                self._save_connection.close()
        except SqlException as e:
            self._logger.exception(f"Failed to close connection to database: {e}")

    def _post_save(self) -> bool:
        try:
            self._logger.info("Adding indexes...")

            cur: Cursor
            with closing(self._save_connection.cursor()) as cur:
                def create_indexes(it: SqliteTable):
                    for sql in it.create_indexes_sql:
                        cur.execute(sql)

                self._database_tables.for_each_table(create_indexes)

            self._logger.info("Indexes added.")
            self._logger.info("Committing...")

            self._save_connection.commit()

            self._logger.info("Done.")
            return True
        except SqlException as e:
            self._logger.exception(f"Failed to finalise the database: {e}")
            return False
        finally:
            self._close_connection()
