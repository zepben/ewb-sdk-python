#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.protection.table_protection_relay_functions import TableProtectionRelayFunctions

__all__ = ["TableCurrentRelays"]


class TableCurrentRelays(TableProtectionRelayFunctions):

    def __init__(self):
        super().__init__()
        self.current_limit_1: Column = self._create_column("current_limit_1", "NUMBER", Nullable.NULL)
        self.inverse_time_flag: Column = self._create_column("inverse_time_flag", "BOOLEAN", Nullable.NULL)
        self.time_delay_1: Column = self._create_column("time_delay_1", "NUMBER", Nullable.NULL)

    @property
    def name(self) -> str:
        return "current_relays"
