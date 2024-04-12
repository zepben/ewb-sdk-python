#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_conducting_equipment import TableConductingEquipment

__all__ = ["TableSeriesCompensators"]


class TableSeriesCompensators(TableConductingEquipment):

    def __init__(self):
        super().__init__()
        self.r: Column = self._create_column("r", "NUMBER", Nullable.NULL)
        self.r0: Column = self._create_column("r0", "NUMBER", Nullable.NULL)
        self.x: Column = self._create_column("x", "NUMBER", Nullable.NULL)
        self.x0: Column = self._create_column("x0", "NUMBER", Nullable.NULL)
        self.varistor_rated_current: Column = self._create_column("varistor_rated_current", "INTEGER", Nullable.NULL)
        self.varistor_voltage_threshold: Column = self._create_column("varistor_voltage_threshold", "INTEGER", Nullable.NULL)

    @property
    def name(self) -> str:
        return "series_compensators"
