#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import Type

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.sqlite_table import SqliteTable, T


class TableVersion(SqliteTable):
    version: Column = None

    SUPPORTED_VERSION = 30

    def __init__(self):
        self.column_index += 1
        self.version = Column(self.column_index, "version", "TEXT", Nullable.NOT_NULL)

    @property
    def table_class(self) -> Type[T]:
        return type(self)

    @property
    def table_class_instance(self) -> T:
        return self

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
