#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from abc import ABC

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_power_system_resources import TablePowerSystemResources

__all__ = ["TableProtectionRelayFunctions"]


class TableProtectionRelayFunctions(TablePowerSystemResources, ABC):

    def __init__(self):
        super().__init__()
        self.model: Column = self._create_column("model", "TEXT", Nullable.NULL)
        self.reclosing: Column = self._create_column("reclosing", "BOOLEAN", Nullable.NULL)
        self.relay_delay_time: Column = self._create_column("relay_delay_time", "NUMBER", Nullable.NULL)
        self.protection_kind: Column = self._create_column("protection_kind", "TEXT", Nullable.NOT_NULL)
        self.directable: Column = self._create_column("directable", "BOOLEAN", Nullable.NULL)
        self.power_direction: Column = self._create_column("power_direction", "TEXT", Nullable.NOT_NULL)
        self.relay_info_mrid: Column = self._create_column("relay_info_mrid", "TEXT", Nullable.NULL)
