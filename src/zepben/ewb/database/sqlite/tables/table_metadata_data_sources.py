#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["TableMetadataDataSources"]

from zepben.ewb.database.sql.column import Column, Nullable
from zepben.ewb.database.sqlite.tables.sqlite_table import SqliteTable


class TableMetadataDataSources(SqliteTable):

    def __init__(self):
        self.source: Column = self._create_column("source", "TEXT", Nullable.NOT_NULL)
        self.version: Column = self._create_column("version", "TEXT", Nullable.NOT_NULL)
        self.timestamp: Column = self._create_column("timestamp", "TEXT", Nullable.NOT_NULL)

    @property
    def name(self) -> str:
        return "metadata_data_sources"
