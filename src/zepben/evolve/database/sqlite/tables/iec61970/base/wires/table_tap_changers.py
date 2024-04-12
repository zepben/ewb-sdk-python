#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from abc import ABC

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_power_system_resources import TablePowerSystemResources

__all__ = ["TableTapChangers"]


class TableTapChangers(TablePowerSystemResources, ABC):

    def __init__(self):
        super().__init__()
        self.control_enabled: Column = self._create_column("control_enabled", "BOOLEAN", Nullable.NOT_NULL)
        self.high_step: Column = self._create_column("high_step", "INTEGER", Nullable.NULL)
        self.low_step: Column = self._create_column("low_step", "INTEGER", Nullable.NULL)
        self.neutral_step: Column = self._create_column("neutral_step", "INTEGER", Nullable.NULL)
        self.neutral_u: Column = self._create_column("neutral_u", "INTEGER", Nullable.NULL)
        self.normal_step: Column = self._create_column("normal_step", "INTEGER", Nullable.NULL)
        self.step: Column = self._create_column("step", "NUMBER", Nullable.NULL)
        self.tap_changer_control_mrid: Column = self._create_column("tap_changer_control_mrid", "TEXT", Nullable.NULL)
