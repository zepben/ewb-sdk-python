#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["TableChangeSetMembers"]

from abc import ABC

from zepben.ewb.database.sql.column import Column, Nullable, Type
from zepben.ewb.database.sqlite.tables.sqlite_table import SqliteTable


class TableChangeSetMembers(SqliteTable, ABC):
    """
    A class representing the ChangeSetMember columns required for the database table.
    """

    def __init__(self):
        super().__init__()
        self.change_set_mrid: Column = self._create_column("change_set_mrid", Type.STRING, Nullable.NOT_NULL)
        self.target_object_mrid: Column = self._create_column("target_object_mrid", Type.STRING, Nullable.NOT_NULL)

    @property
    def unique_index_columns(self):
        yield [self.change_set_mrid, self.target_object_mrid]

    @property
    def non_unique_index_columns(self):
        yield [self.target_object_mrid]
        yield [self.change_set_mrid]
