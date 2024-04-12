#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.generation.production.table_power_electronics_units import TablePowerElectronicsUnits

__all__ = ["TableBatteryUnits"]


class TableBatteryUnits(TablePowerElectronicsUnits):

    def __init__(self):
        super().__init__()
        self.battery_state: Column = self._create_column("battery_state", "TEXT", Nullable.NOT_NULL)
        self.rated_e: Column = self._create_column("rated_e", "INTEGER", Nullable.NULL)
        self.stored_e: Column = self._create_column("stored_e", "INTEGER", Nullable.NULL)

    @property
    def name(self) -> str:
        return "battery_units"
