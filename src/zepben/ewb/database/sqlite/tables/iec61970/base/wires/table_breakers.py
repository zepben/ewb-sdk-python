#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["TableBreakers"]

from zepben.ewb.database.sql.column import Column, Nullable
from zepben.ewb.database.sqlite.tables.iec61970.base.wires.table_protected_switches import TableProtectedSwitches


class TableBreakers(TableProtectedSwitches):

    @property
    def name(self) -> str:
        return "breakers"

    def __init__(self):
        super().__init__()
        self.in_transit_time: Column = self._create_column("in_transit_time", "NUMBER", Nullable.NULL)
