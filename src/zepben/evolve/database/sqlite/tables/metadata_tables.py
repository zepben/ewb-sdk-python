#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.sqlite_table import SqliteTable

__all__ = ["TableVersion", "TableMetadataSources"]


class TableVersion(SqliteTable):
    version: Column = None

    SUPPORTED_VERSION = 30

    def __init__(self):
        self.column_index += 1
        self.version = Column(self.column_index, "version", "TEXT", Nullable.NOT_NULL)

    def name(self) -> str:
        return "version"


class TableMetadataSources(SqliteTable):
    source: Column = None
    version: Column = None
    timestamp: Column = None

    def __init__(self):
        self.column_index += 1
        self.source = Column(self.column_index, "source", "TEXT", Nullable.NOT_NULL)
        self.column_index += 1
        self.version = Column(self.column_index, "version", "TEXT", Nullable.NOT_NULL)
        self.column_index += 1
        self.timestamp = Column(self.column_index, "timestamp", "TEXT", Nullable.NOT_NULL)

    def name(self) -> str:
        return "metadata_data_sources"
