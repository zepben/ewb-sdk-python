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

    def __init__(self):
        self._column_index += 1
        self.version = Column(self._column_index, "version", "TEXT", Nullable.NOT_NULL)

    @property
    def SUPPORTED_VERSION(self):
        return 27

    @property
    def table_class(self) -> Type[T]:
        return type(self)

    @property
    def table_class_instance(self) -> T:
        return self

    def name(self) -> str:
        return "version"

