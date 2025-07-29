#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["TableProtectionRelaySchemes"]

from zepben.ewb.database.sql.column import Column, Nullable
from zepben.ewb.database.sqlite.tables.iec61970.base.core.table_identified_objects import TableIdentifiedObjects


class TableProtectionRelaySchemes(TableIdentifiedObjects):

    def __init__(self):
        super().__init__()
        self.system_mrid: Column = self._create_column("system_mrid", "TEXT", Nullable.NULL)

    @property
    def name(self) -> str:
        return "protection_relay_schemes"
