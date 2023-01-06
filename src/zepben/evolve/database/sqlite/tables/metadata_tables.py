#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.sqlite_table import SqliteTable

__all__ = ["TableVersion", "TableMetadataDataSources"]


class TableVersion(SqliteTable):
    version: Column = None

    SUPPORTED_VERSION = 43

    def __init__(self):
        self.version = self._create_column("version", "TEXT", Nullable.NOT_NULL)

    def name(self) -> str:
        return "version"


class TableMetadataDataSources(SqliteTable):
    source: Column = None
    version: Column = None
    timestamp: Column = None

    def __init__(self):
        self.source = self._create_column("source", "TEXT", Nullable.NOT_NULL)
        self.version = self._create_column("version", "TEXT", Nullable.NOT_NULL)
        self.timestamp = self._create_column("timestamp", "TEXT", Nullable.NOT_NULL)

    def name(self) -> str:
        return "metadata_data_sources"
