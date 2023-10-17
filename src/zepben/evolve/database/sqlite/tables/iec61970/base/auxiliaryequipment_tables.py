#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.core_tables import TableEquipment

__all__ = ["TableAuxiliaryEquipment", "TableSensors", "TableCurrentTransformers", "TableFaultIndicators", "TablePotentialTransformers"]


# noinspection PyAbstractClass
class TableAuxiliaryEquipment(TableEquipment):
    terminal_mrid: Column = None

    def __init__(self):
        super(TableAuxiliaryEquipment, self).__init__()
        self.terminal_mrid = self._create_column("terminal_mrid", "TEXT", Nullable.NULL)


# noinspection PyAbstractClass
class TableSensors(TableAuxiliaryEquipment):
    pass


class TableCurrentTransformers(TableSensors):
    current_transformer_info_mrid: Column = None
    core_burden: Column = None

    def __init__(self):
        super(TableCurrentTransformers, self).__init__()
        self.current_transformer_info_mrid = self._create_column("current_transformer_info_mrid", "TEXT", Nullable.NULL)
        self.core_burden = self._create_column("core_burden", "INTEGER", Nullable.NULL)

    def name(self) -> str:
        return "current_transformers"


class TableFaultIndicators(TableAuxiliaryEquipment):

    def name(self) -> str:
        return "fault_indicators"


class TablePotentialTransformers(TableSensors):
    potential_transformer_info_mrid: Column = None
    type: Column = None

    def __init__(self):
        super(TablePotentialTransformers, self).__init__()
        self.potential_transformer_info_mrid = self._create_column("potential_transformer_info_mrid", "TEXT", Nullable.NULL)
        self.type = self._create_column("type", "TEXT", Nullable.NOT_NULL)

    def name(self) -> str:
        return "potential_transformers"
