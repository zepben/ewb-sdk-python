#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import List

from zepben.evolve.database.sqlite.tables.column import Nullable, Column
from zepben.evolve.database.sqlite.tables.iec61970.base.core_tables import TableIdentifiedObjects, TableEquipmentContainers
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.container_tables import TableLines

__all__ = ["TableCircuits", "TableLoops", "TableLvFeeders"]


class TableCircuits(TableLines):
    loop_mrid: Column = None

    def __init__(self):
        super(TableCircuits, self).__init__()
        self.loop_mrid = self._create_column("loop_mrid", "TEXT", Nullable.NULL)

    def name(self) -> str:
        return "circuits"

    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableCircuits, self).non_unique_index_columns()
        cols.append([self.loop_mrid])
        return cols


class TableLoops(TableIdentifiedObjects):
    def name(self) -> str:
        return "loops"


class TableLvFeeders(TableEquipmentContainers):
    normal_head_terminal_mrid: Column = None

    def __init__(self):
        super(TableLvFeeders, self).__init__()
        self.normal_head_terminal_mrid = self._create_column("normal_head_terminal_mrid", "TEXT", Nullable.NULL)

    def name(self) -> str:
        return "lv_feeders"
