#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_regulating_controls import TableRegulatingControls

__all__ = ["TableTapChangerControls"]


class TableTapChangerControls(TableRegulatingControls):

    def __init__(self):
        super().__init__()
        self.limit_voltage: Column = self._create_column("limit_voltage", "INTEGER", Nullable.NULL)
        self.line_drop_compensation: Column = self._create_column("line_drop_compensation", "BOOLEAN", Nullable.NULL)
        self.line_drop_r: Column = self._create_column("line_drop_r", "NUMBER", Nullable.NULL)
        self.line_drop_x: Column = self._create_column("line_drop_x", "NUMBER", Nullable.NULL)
        self.reverse_line_drop_r: Column = self._create_column("reverse_line_drop_r", "NUMBER", Nullable.NULL)
        self.reverse_line_drop_x: Column = self._create_column("reverse_line_drop_x", "NUMBER", Nullable.NULL)
        self.forward_ldc_blocking: Column = self._create_column("forward_ldc_blocking", "BOOLEAN", Nullable.NULL)
        self.time_delay: Column = self._create_column("time_delay", "NUMBER", Nullable.NULL)
        self.co_generation_enabled: Column = self._create_column("co_generation_enabled", "BOOLEAN", Nullable.NULL)

    @property
    def name(self) -> str:
        return "tap_changer_controls"
