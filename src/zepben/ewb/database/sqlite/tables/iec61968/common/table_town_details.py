#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["TableTownDetails"]

from abc import ABC

from zepben.ewb.database.sql.column import Column, Nullable
from zepben.ewb.database.sqlite.tables.sqlite_table import SqliteTable


class TableTownDetails(SqliteTable, ABC):

    def __init__(self):
        super().__init__()
        self.town_name: Column = self._create_column("town_name", "TEXT", Nullable.NULL)
        self.state_or_province: Column = self._create_column("state_or_province", "TEXT", Nullable.NULL)
