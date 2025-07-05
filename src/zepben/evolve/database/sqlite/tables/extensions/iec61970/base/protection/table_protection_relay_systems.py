#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_equipment import TableEquipment

__all__ = ["TableProtectionRelaySystems"]


class TableProtectionRelaySystems(TableEquipment):

    def __init__(self):
        super().__init__()
        self.protection_kind: Column = self._create_column("protection_kind", "TEXT", Nullable.NOT_NULL)

    @property
    def name(self) -> str:
        return "protection_relay_systems"
