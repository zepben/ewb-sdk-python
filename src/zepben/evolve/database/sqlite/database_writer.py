#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import logging
import os
import sqlite3
from contextlib import contextmanager
from typing import Generator, Set, List

from dataclassy import dataclass

from zepben.evolve import DatabaseTables, MetadataCollection, BaseService, TableVersion, MetadataCollectionWriter, MetadataEntryWriter, NetworkService, \
    NetworkServiceWriter, NetworkCIMWriter, DiagramService, CustomerService, CustomerCIMWriter
from zepben.evolve.database.sqlite.writers.customer_service_writer import CustomerServiceWriter
from zepben.evolve.database.sqlite.writers.diagram_cim_writer import DiagramCIMWriter
from zepben.evolve.database.sqlite.writers.diagram_service_writer import DiagramServiceWriter

__all__ = ["DatabaseWriter", "connection", "cursor"]

logger = logging.getLogger("DatabaseWriter")


@contextmanager
def connection(connection_string: str) -> sqlite3.Connection:
    try:
        conn = sqlite3.connect(connection_string)
        conn.isolation_level = None  # autocommit off
        yield conn
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        logger.error(f"Failed to connect to the database for saving: {e}")
        return None


@contextmanager
def cursor(conn: sqlite3.Connection) -> Generator[sqlite3.Cursor, None, None]:
    cur = conn.cursor()
    cur.execute("PRAGMA journal_mode = OFF")
    cur.execute("PRAGMA synchronous = OFF")
    yield cur
    cur.close()


@dataclass(slots=True)
class DatabaseWriter(object):
    database_path: str
    _database_tables: DatabaseTables = DatabaseTables()

    _saved_common_mrids: Set[str] = set()
    _has_been_used: bool = False

    def save(self, metadata_collection: MetadataCollection, services: List[BaseService]) -> bool:
        if not services:
            logger.warning("No services were provided, therefore there is nothing to save")
            return False

        if self._has_been_used:
            logger.error("You can only use the database writer once.")
            return False

        self._has_been_used = True

        if not self._pre_save():
            return False

        with connection(self.database_path) as conn:
            if not self._create(conn):
                return False

            with cursor(conn) as c:
                # noinspection PyArgumentList
                status = MetadataCollectionWriter().save(metadata_collection, MetadataEntryWriter(self._database_tables, c))

                for service in services:
                    try:
                        if isinstance(service, NetworkService):
                            # noinspection PyArgumentList
                            status = status and NetworkServiceWriter(self.has_common, self.add_common).save(service, NetworkCIMWriter(self._database_tables, c))
                        elif isinstance(service, CustomerService):
                            # noinspection PyArgumentList
                            status = status and \
                                     CustomerServiceWriter(self.has_common, self.add_common).save(service, CustomerCIMWriter(self._database_tables, c))
                        elif isinstance(service, DiagramService):
                            # noinspection PyArgumentList
                            status = status and DiagramServiceWriter(self.has_common, self.add_common).save(service, DiagramCIMWriter(self._database_tables, c))
                        else:
                            logger.error(f"Unsupported service of type {service.__class__.__name__} couldn't be saved.")
                            status = False
                    except Exception as e:
                        logger.error(f"Unable to save database: {e}")
                        status = False

            return status and self._post_save(conn)
        # connection closed here

    def add_common(self, mrid: str) -> bool:
        self._saved_common_mrids.add(mrid)
        return True

    def has_common(self, mrid: str) -> bool:
        return mrid in self._saved_common_mrids

    def _pre_save(self) -> bool:
        return self._remove_existing()

    def _remove_existing(self) -> bool:
        try:
            if os.path.isfile(self.database_path):
                os.remove(self.database_path)
            return True
        except Exception as e:
            logger.error(f"Unable to save database, failed to remove previous instance: {e}")
            return False

    def _create(self, conn: sqlite3.Connection) -> bool:
        try:
            version_table = self._database_tables.get_table(TableVersion)
            logger.info(f"Creating database schema v{version_table.SUPPORTED_VERSION}")

            with cursor(conn) as c:
                for table in self._database_tables.tables:
                    c.execute(table.create_table_sql())

                c.execute(version_table.prepared_insert_sql(), (version_table.SUPPORTED_VERSION,))

            conn.commit()
            logger.info("Database saved.")
            return True
        except sqlite3.Error as e:
            logger.error(f"Failed to create database schema {e}")
            return False

    def _post_save(self, conn) -> bool:
        try:
            with cursor(conn) as c:
                for table in self._database_tables.tables:
                    for index_sql in table.create_indexes_sql():
                        c.execute(index_sql)
            conn.commit()
            return True
        except sqlite3.Error as e:
            logger.error(f"Failed to create indexes and finalise the database: {e}")
            return False
