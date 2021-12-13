#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.core_tables import TableEquipment

__all__ = ["TableAuxiliaryEquipment", "TableFaultIndicators"]


# noinspection PyAbstractClass
class TableAuxiliaryEquipment(TableEquipment):
    terminal_mrid: Column = None

    def __init__(self):
        super(TableAuxiliaryEquipment, self).__init__()
        self.terminal_mrid = self._create_column("terminal_mrid", "TEXT", Nullable.NULL)


class TableFaultIndicators(TableAuxiliaryEquipment):

    def name(self) -> str:
        return "fault_indicators"
