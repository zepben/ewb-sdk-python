#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["TableLvFeeders"]

from zepben.ewb.database.sql.column import Column, Nullable
from zepben.ewb.database.sqlite.tables.iec61970.base.core.table_equipment_containers import TableEquipmentContainers


class TableLvFeeders(TableEquipmentContainers):

    def __init__(self):
        super().__init__()
        self.normal_head_terminal_mrid: Column = self._create_column("normal_head_terminal_mrid", "TEXT", Nullable.NULL)

    @property
    def name(self) -> str:
        return "lv_feeders"
