#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_energy_connections import TableEnergyConnections

__all__ = ["TableEnergyConsumers"]


class TableEnergyConsumers(TableEnergyConnections):

    def __init__(self):
        super().__init__()
        self.customer_count: Column = self._create_column("customer_count", "INTEGER", Nullable.NULL)
        self.grounded: Column = self._create_column("grounded", "BOOLEAN", Nullable.NOT_NULL)
        self.p: Column = self._create_column("p", "NUMBER", Nullable.NULL)
        self.q: Column = self._create_column("q", "NUMBER", Nullable.NULL)
        self.p_fixed: Column = self._create_column("p_fixed", "NUMBER", Nullable.NULL)
        self.q_fixed: Column = self._create_column("q_fixed", "NUMBER", Nullable.NULL)
        self.phase_connection: Column = self._create_column("phase_connection", "TEXT", Nullable.NOT_NULL)

    @property
    def name(self) -> str:
        return "energy_consumers"
