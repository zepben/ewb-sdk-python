#  Copyright 2024 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import List

from zepben.evolve import SqliteTable, Column, Nullable

__all__ = ["TableProtectionRelayFunctionsSensors"]


class TableProtectionRelayFunctionsSensors(SqliteTable):
    protection_relay_function_mrid: Column = None
    sensor_mrid: Column = None

    def __init__(self):
        super(TableProtectionRelayFunctionsSensors, self).__init__()
        self.protection_relay_function_mrid = self._create_column("protection_relay_function_mrid", "TEXT", Nullable.NOT_NULL)
        self.sensor_mrid = self._create_column("sensor_mrid", "TEXT", Nullable.NOT_NULL)

    def name(self) -> str:
        return "protection_relay_functions_sensors"

    def unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableProtectionRelayFunctionsSensors, self).unique_index_columns()
        cols.append([self.protection_relay_function_mrid, self.sensor_mrid])
        return cols

    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableProtectionRelayFunctionsSensors, self).non_unique_index_columns()
        cols.append([self.protection_relay_function_mrid])
        cols.append([self.sensor_mrid])
        return cols
