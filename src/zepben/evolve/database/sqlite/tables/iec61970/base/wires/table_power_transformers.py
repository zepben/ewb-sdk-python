#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_conducting_equipment import TableConductingEquipment

__all__ = ["TablePowerTransformers"]


class TablePowerTransformers(TableConductingEquipment):

    def __init__(self):
        super().__init__()
        self.vector_group: Column = self._create_column("vector_group", "TEXT", Nullable.NOT_NULL)
        self.transformer_utilisation: Column = self._create_column("transformer_utilisation", "NUMBER", Nullable.NULL)
        self.construction_kind: Column = self._create_column("construction_kind", "TEXT", Nullable.NOT_NULL)
        self.function: Column = self._create_column("function", "TEXT", Nullable.NOT_NULL)
        self.power_transformer_info_mrid: Column = self._create_column("power_transformer_info_mrid", "TEXT", Nullable.NULL)

    @property
    def name(self) -> str:
        return "power_transformers"
