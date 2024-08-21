#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from abc import ABC

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_equipment import TableEquipment

__all__ = ["TableConductingEquipment"]


class TableConductingEquipment(TableEquipment, ABC):

    def __init__(self):
        super().__init__()
        self.base_voltage_mrid: Column = self._create_column("base_voltage_mrid", "TEXT", Nullable.NULL)
