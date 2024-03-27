#  Copyright 2024 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import List

from zepben.evolve import SqliteTable
from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.core_tables import TableEquipment, TableIdentifiedObjects, TablePowerSystemResources

__all__ = ["TableProtectionRelayFunctions", "TableCurrentRelays", "TableProtectionRelaySystems", "TableDistanceRelays",
           "TableProtectionRelayFunctionThresholds", "TableProtectionRelayFunctionTimeLimits", "TableProtectionRelaySchemes", "TableVoltageRelays"]


# noinspection PyAbstractClass
class TableProtectionRelayFunctions(TablePowerSystemResources):
    model: Column = None
    reclosing: Column = None
    relay_delay_time: Column = None
    protection_kind: Column = None
    directable: Column = None
    power_direction: Column = None
    relay_info_mrid: Column = None

    def __init__(self):
        super(TableProtectionRelayFunctions, self).__init__()
        self.model = self._create_column("model", "TEXT", Nullable.NULL)
        self.reclosing = self._create_column("reclosing", "BOOLEAN", Nullable.NULL)
        self.relay_delay_time = self._create_column("relay_delay_time", "NUMBER", Nullable.NULL)
        self.protection_kind = self._create_column("protection_kind", "TEXT", Nullable.NOT_NULL)
        self.directable = self._create_column("directable", "BOOLEAN", Nullable.NULL)
        self.power_direction = self._create_column("power_direction", "TEXT", Nullable.NOT_NULL)
        self.relay_info_mrid = self._create_column("relay_info_mrid", "TEXT", Nullable.NULL)


class TableCurrentRelays(TableProtectionRelayFunctions):
    current_limit_1: Column = None
    inverse_time_flag: Column = None
    time_delay_1: Column = None

    def __init__(self):
        super(TableCurrentRelays, self).__init__()
        self.current_limit_1 = self._create_column("current_limit_1", "NUMBER", Nullable.NULL)
        self.inverse_time_flag = self._create_column("inverse_time_flag", "BOOLEAN", Nullable.NULL)
        self.time_delay_1 = self._create_column("time_delay_1", "NUMBER", Nullable.NULL)

    def name(self) -> str:
        return "current_relays"


class TableDistanceRelays(TableProtectionRelayFunctions):
    backward_blind: Column = None
    backward_reach: Column = None
    backward_reactance: Column = None
    forward_blind: Column = None
    forward_reach: Column = None
    forward_reactance: Column = None
    operation_phase_angle1: Column = None
    operation_phase_angle2: Column = None
    operation_phase_angle3: Column = None

    def __init__(self):
        super(TableDistanceRelays, self).__init__()
        self.backward_blind = self._create_column("backward_blind", "NUMBER", Nullable.NULL)
        self.backward_reach = self._create_column("backward_reach", "NUMBER", Nullable.NULL)
        self.backward_reactance = self._create_column("backward_reactance", "NUMBER", Nullable.NULL)
        self.forward_blind = self._create_column("forward_blind", "NUMBER", Nullable.NULL)
        self.forward_reach = self._create_column("forward_reach", "NUMBER", Nullable.NULL)
        self.forward_reactance = self._create_column("forward_reactance", "NUMBER", Nullable.NULL)
        self.operation_phase_angle1 = self._create_column("operation_phase_angle1", "NUMBER", Nullable.NULL)
        self.operation_phase_angle2 = self._create_column("operation_phase_angle2", "NUMBER", Nullable.NULL)
        self.operation_phase_angle3 = self._create_column("operation_phase_angle3", "NUMBER", Nullable.NULL)

    def name(self) -> str:
        return "distance_relays"


class TableProtectionRelayFunctionThresholds(SqliteTable):
    protection_relay_function_mrid: Column = None
    sequence_number: Column = None
    unit_symbol: Column = None
    value: Column = None
    name_: Column = None

    def __init__(self):
        super(TableProtectionRelayFunctionThresholds, self).__init__()
        self.protection_relay_function_mrid = self._create_column("protection_relay_function_mrid", "TEXT", Nullable.NOT_NULL)
        self.sequence_number = self._create_column("sequence_number", "INTEGER", Nullable.NOT_NULL)
        self.unit_symbol = self._create_column("unit_symbol", "TEXT", Nullable.NOT_NULL)
        self.value = self._create_column("value", "NUMBER", Nullable.NOT_NULL)
        self.name_ = self._create_column("name", "TEXT", Nullable.NULL)

    def name(self) -> str:
        return "protection_relay_function_thresholds"

    def unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableProtectionRelayFunctionThresholds, self).unique_index_columns()
        cols.append([self.protection_relay_function_mrid, self.sequence_number])
        return cols

    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableProtectionRelayFunctionThresholds, self).non_unique_index_columns()
        cols.append([self.protection_relay_function_mrid])
        return cols


class TableProtectionRelayFunctionTimeLimits(SqliteTable):
    protection_relay_function_mrid: Column = None
    sequence_number: Column = None
    time_limit: Column = None

    def __init__(self):
        super(TableProtectionRelayFunctionTimeLimits, self).__init__()
        self.protection_relay_function_mrid = self._create_column("protection_relay_function_mrid", "TEXT", Nullable.NOT_NULL)
        self.sequence_number = self._create_column("sequence_number", "INTEGER", Nullable.NOT_NULL)
        self.time_limit = self._create_column("time_limit", "NUMBER", Nullable.NOT_NULL)

    def name(self) -> str:
        return "protection_relay_function_time_limits"

    def unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableProtectionRelayFunctionTimeLimits, self).unique_index_columns()
        cols.append([self.protection_relay_function_mrid, self.sequence_number])
        return cols

    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableProtectionRelayFunctionTimeLimits, self).non_unique_index_columns()
        cols.append([self.protection_relay_function_mrid])
        return cols


class TableProtectionRelaySchemes(TableIdentifiedObjects):
    system_mrid: Column = None

    def __init__(self):
        super(TableProtectionRelaySchemes, self).__init__()
        self.system_mrid = self._create_column("system_mrid", "TEXT", Nullable.NULL)

    def name(self) -> str:
        return "protection_relay_schemes"


class TableProtectionRelaySystems(TableEquipment):
    protection_kind: Column = None

    def __init__(self):
        super(TableProtectionRelaySystems, self).__init__()
        self.protection_kind = self._create_column("protection_kind", "TEXT", Nullable.NOT_NULL)

    def name(self) -> str:
        return "protection_relay_systems"


class TableVoltageRelays(TableProtectionRelayFunctions):
    def name(self) -> str:
        return "voltage_relays"
