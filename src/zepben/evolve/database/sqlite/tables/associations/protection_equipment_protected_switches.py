#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import List

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.sqlite_table import SqliteTable

__all__ = ["TableProtectionEquipmentProtectedSwitches"]


class TableProtectionEquipmentProtectedSwitches(SqliteTable):
    protection_equipment_mrid: Column = None
    protected_switch_mrid: Column = None

    def __init__(self):
        super(TableProtectionEquipmentProtectedSwitches, self).__init__()
        self.protection_equipment_mrid = self._create_column("protection_equipment_mrid", "TEXT", Nullable.NOT_NULL)
        self.protected_switch_mrid = self._create_column("protected_switch_mrid", "TEXT", Nullable.NOT_NULL)

    def name(self) -> str:
        return "protection_equipment_protected_switches"

    def unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableProtectionEquipmentProtectedSwitches, self).unique_index_columns()
        cols.append([self.protection_equipment_mrid, self.protected_switch_mrid])
        return cols

    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableProtectionEquipmentProtectedSwitches, self).non_unique_index_columns()
        cols.append([self.protection_equipment_mrid])
        cols.append([self.protected_switch_mrid])
        return cols
