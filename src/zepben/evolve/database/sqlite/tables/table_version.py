#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import sqlite3
from sqlite3 import Cursor
from typing import Optional

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.sqlite_table import SqliteTable


__all__ = ["TableVersion"]


class TableVersion(SqliteTable):
    SUPPORTED_VERSION = 56

    def __init__(self):
        self.version: Column = self._create_column("version", "TEXT", Nullable.NOT_NULL)

    @property
    def name(self) -> str:
        return "version"

    def get_version(self, cur: Cursor) -> Optional[int]:
        """
        Helper function to read the version from the database.
        """
        try:
            cur.execute(self.select_sql)
            rows = cur.fetchall()
            if len(rows) == 1:
                return int(rows[0][0])
        except sqlite3.Error:
            pass

        return None
