#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from abc import ABC

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_power_system_resources import TablePowerSystemResources

__all__ = ["TableRegulatingControls"]


class TableRegulatingControls(TablePowerSystemResources, ABC):

    def __init__(self):
        super().__init__()
        self.discrete: Column = self._create_column("discrete", "BOOLEAN", Nullable.NULL)
        self.mode: Column = self._create_column("mode", "TEXT", Nullable.NOT_NULL)
        self.monitored_phase: Column = self._create_column("monitored_phase", "TEXT", Nullable.NOT_NULL)
        self.target_deadband: Column = self._create_column("target_deadband", "NUMBER", Nullable.NULL)
        self.target_value: Column = self._create_column("target_value", "NUMBER", Nullable.NULL)
        self.enabled: Column = self._create_column("enabled", "BOOLEAN", Nullable.NULL)
        self.max_allowed_target_value: Column = self._create_column("max_allowed_target_value", "NUMBER", Nullable.NULL)
        self.min_allowed_target_value: Column = self._create_column("min_allowed_target_value", "NUMBER", Nullable.NULL)
        self.rated_current: Column = self._create_column("rated_current", "NUMBER", Nullable.NULL)
        self.terminal_mrid: Column = self._create_column("terminal_mrid", "TEXT", Nullable.NULL)
        self.ct_primary: Column = self._create_column("ct_primary", "NUMBER", Nullable.NULL)
        self.min_target_deadband: Column = self._create_column("min_target_deadband", "NUMBER", Nullable.NULL)
