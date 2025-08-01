#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["TableBatteryControls"]

from zepben.ewb.database.sqlite.tables.column import Column, Nullable
from zepben.ewb.database.sqlite.tables.iec61970.base.wires.table_regulating_controls import TableRegulatingControls


class TableBatteryControls(TableRegulatingControls):

    def __init__(self):
        super().__init__()
        self.charging_rate: Column = self._create_column("charging_rate", "NUMBER", Nullable.NULL)
        self.discharging_rate: Column = self._create_column("discharging_rate", "NUMBER", Nullable.NULL)
        self.reserve_percent: Column = self._create_column("reserve_percent", "NUMBER", Nullable.NULL)
        self.control_mode: Column = self._create_column("control_mode", "TEXT", Nullable.NOT_NULL)

    @property
    def name(self) -> str:
        return "battery_controls"
