#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_shunt_compensators import TableShuntCompensators

__all__ = ["TableLinearShuntCompensators"]


class TableLinearShuntCompensators(TableShuntCompensators):

    def __init__(self):
        super().__init__()
        self.b0_per_section: Column = self._create_column("b0_per_section", "NUMBER", Nullable.NULL)
        self.b_per_section: Column = self._create_column("b_per_section", "NUMBER", Nullable.NULL)
        self.g0_per_section: Column = self._create_column("g0_per_section", "NUMBER", Nullable.NULL)
        self.g_per_section: Column = self._create_column("g_per_section", "NUMBER", Nullable.NULL)

    @property
    def name(self) -> str:
        return "linear_shunt_compensators"
