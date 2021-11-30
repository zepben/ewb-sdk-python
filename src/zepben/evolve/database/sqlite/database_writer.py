#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import sqlite3
from contextlib import contextmanager
from typing import Generator, Callable, Set, List

from dataclassy import dataclass

from zepben.evolve import DatabaseTables, MetadataCollection, BaseService


@contextmanager
def connection(connection_string: str) -> sqlite3.Connection:
    conn = sqlite3.connect(connection_string)
    conn.isolation_level = None  # autocommit off
    yield conn
    conn.commit()
    conn.close()


@contextmanager
def cursor(connection: sqlite3.Connection) -> Generator[sqlite3.Cursor, None, None]:
    cur = connection.cursor()
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
        pass




