#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_energy_connections import TableEnergyConnections

__all__ = ["TableEnergySources"]


class TableEnergySources(TableEnergyConnections):

    def __init__(self):
        super().__init__()
        self.active_power: Column = self._create_column("active_power", "NUMBER", Nullable.NULL)
        self.reactive_power: Column = self._create_column("reactive_power", "NUMBER", Nullable.NULL)
        self.voltage_angle: Column = self._create_column("voltage_angle", "NUMBER", Nullable.NULL)
        self.voltage_magnitude: Column = self._create_column("voltage_magnitude", "NUMBER", Nullable.NULL)
        self.p_max: Column = self._create_column("p_max", "NUMBER", Nullable.NULL)
        self.p_min: Column = self._create_column("p_min", "NUMBER", Nullable.NULL)
        self.r: Column = self._create_column("r", "NUMBER", Nullable.NULL)
        self.r0: Column = self._create_column("r0", "NUMBER", Nullable.NULL)
        self.rn: Column = self._create_column("rn", "NUMBER", Nullable.NULL)
        self.x: Column = self._create_column("x", "NUMBER", Nullable.NULL)
        self.x0: Column = self._create_column("x0", "NUMBER", Nullable.NULL)
        self.xn: Column = self._create_column("xn", "NUMBER", Nullable.NULL)
        self.is_external_grid: Column = self._create_column("is_external_grid", "BOOLEAN", Nullable.NOT_NULL)
        self.r_min: Column = self._create_column("r_min", "NUMBER", Nullable.NULL)
        self.rn_min: Column = self._create_column("rn_min", "NUMBER", Nullable.NULL)
        self.r0_min: Column = self._create_column("r0_min", "NUMBER", Nullable.NULL)
        self.x_min: Column = self._create_column("x_min", "NUMBER", Nullable.NULL)
        self.xn_min: Column = self._create_column("xn_min", "NUMBER", Nullable.NULL)
        self.x0_min: Column = self._create_column("x0_min", "NUMBER", Nullable.NULL)
        self.r_max: Column = self._create_column("r_max", "NUMBER", Nullable.NULL)
        self.rn_max: Column = self._create_column("rn_max", "NUMBER", Nullable.NULL)
        self.r0_max: Column = self._create_column("r0_max", "NUMBER", Nullable.NULL)
        self.x_max: Column = self._create_column("x_max", "NUMBER", Nullable.NULL)
        self.xn_max: Column = self._create_column("xn_max", "NUMBER", Nullable.NULL)
        self.x0_max: Column = self._create_column("x0_max", "NUMBER", Nullable.NULL)

    @property
    def name(self) -> str:
        return "energy_sources"
