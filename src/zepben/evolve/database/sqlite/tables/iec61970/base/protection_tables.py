#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.core_tables import TableEquipment, TableIdentifiedObjects

__all__ = ["TableProtectionEquipment", "TableCurrentRelays"]


# noinspection PyAbstractClass
class TableProtectionEquipment(TableEquipment):
    relay_delay_time: Column = None
    protection_kind: Column = None
    directable: Column = None
    power_direction: Column = None

    def __init__(self):
        super(TableProtectionEquipment, self).__init__()
        self.relay_delay_time = self._create_column("relay_delay_time", "NUMBER", Nullable.NULL)
        self.protection_kind = self._create_column("protection_kind", "TEXT", Nullable.NOT_NULL)
        self.directable = self._create_column("directable", "BOOLEAN", Nullable.NULL)
        self.power_direction = self._create_column("power_direction", "TEXT", Nullable.NOT_NULL)


class TableCurrentRelays(TableProtectionEquipment):
    current_limit_1: Column = None
    inverse_time_flag: Column = None
    time_delay_1: Column = None
    current_relay_info_mrid: Column = None

    def __init__(self):
        super(TableCurrentRelays, self).__init__()
        self.current_limit_1 = self._create_column("current_limit_1", "NUMBER", Nullable.NULL)
        self.inverse_time_flag = self._create_column("inverse_time_flag", "BOOLEAN", Nullable.NULL)
        self.time_delay_1 = self._create_column("time_delay_1", "NUMBER", Nullable.NULL)
        self.current_relay_info_mrid = self._create_column("current_relay_info_mrid", "TEXT", Nullable.NULL)

    def name(self) -> str:
        return "current_relays"
