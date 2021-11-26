#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import List

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61968.asset_tables import TableAssetInfo

__all__ = ["TablePowerTransformerInfo", "TableTransformerEndInfo", "TableTransformerTankInfo", "TableWireInfo", "TableCableInfo", "TableAssetInfo",
           "TableOverheadWireInfo", "TableNoLoadTests", "TableOpenCircuitTests", "TableShortCircuitTests", "TableTransformerTest"]


class TableTransformerTest(TableAssetInfo):
    base_power: Column = None
    temperature: Column = None

    def __init__(self):
        super(TableTransformerTest, self).__init__()
        self.column_index += 1
        self.base_power = Column(self.column_index, "base_power", "INTEGER", Nullable.NULL)
        self.column_index += 1
        self.temperature = Column(self.column_index, "temperature", "NUMBER", Nullable.NULL)


class TableNoLoadTests(TableTransformerTest):
    energized_end_voltage = None
    exciting_current = None
    exciting_current_zero = None
    loss = None
    loss_zero = None

    def name(self) -> str:
        return "no_load_tests"

    def __init__(self):
        super(TableTransformerTest, self).__init__()
        self.column_index += 1
        self.energized_end_voltage = Column(self.column_index, "energised_end_voltage", "INTEGER", Nullable.NULL)
        self.column_index += 1
        self.exciting_current = Column(self.column_index, "exciting_current", "NUMBER", Nullable.NULL)
        self.column_index += 1
        self.exciting_current_zero = Column(self.column_index, "exciting_current_zero", "NUMBER", Nullable.NULL)
        self.column_index += 1
        self.loss = Column(self.column_index, "exciting_current", "NUMBER", Nullable.NULL)
        self.column_index += 1
        self.loss_zero = Column(self.column_index, "loss_zero", "INTEGER", Nullable.NULL)


class TableOpenCircuitTests(TableTransformerTest):
    energized_end_step = None
    energized_end_voltage = None
    open_end_step = None
    open_end_voltage = None
    phase_shift = None

    def name(self) -> str:
        return "open_circuit_tests"

    def __init__(self):
        super(TableTransformerTest, self).__init__()
        self.column_index += 1
        self.energized_end_voltage = Column(self.column_index, "energised_end_step", "INTEGER", Nullable.NULL)
        self.column_index += 1
        self.energized_end_step = Column(self.column_index, "energised_end_voltage", "INTEGER", Nullable.NULL)
        self.column_index += 1
        self.open_end_step = Column(self.column_index, "open_end_step", "INTEGER", Nullable.NULL)
        self.column_index += 1
        self.open_end_voltage = Column(self.column_index, "open_end_voltage", "INTEGER", Nullable.NULL)
        self.column_index += 1
        self.phase_shift = Column(self.column_index, "phase_shift", "NUMBER", Nullable.NULL)


class TablePowerTransformerInfo(TableAssetInfo):

    def name(self) -> str:
        return "short_circuit_tests"


class TableShortCircuitTests(TableTransformerTest):
    current = None
    energized_end_voltage = None
    grounded_end_step = None
    leakage_impedance = None
    leakage_impedance_zero = None
    loss = None
    loss_zero = None
    power = None
    voltage = None
    voltage_ohmic_part = None

    def name(self) -> str:
        return "short_circuit_tests"

    def __init__(self):
        super(TableTransformerTest, self).__init__()
        self.column_index += 1
        self.current = Column(self.column_index, "current", "NUMBER", Nullable.NULL)
        self.column_index += 1
        self.energized_end_voltage = Column(self.column_index, "energized_end_voltage", "INTEGER", Nullable.NULL)
        self.column_index += 1
        self.grounded_end_step = Column(self.column_index, "grounded_end_step", "INTEGER", Nullable.NULL)
        self.column_index += 1
        self.leakage_impedance = Column(self.column_index, "leakage_impedance", "NUMBER", Nullable.NULL)
        self.column_index += 1
        self.leakage_impedance_zero = Column(self.column_index, "leakage_impedance_zero", "NUMBER", Nullable.NULL)
        self.column_index += 1
        self.loss = Column(self.column_index, "loss", "INTEGER", Nullable.NULL)
        self.column_index += 1
        self.loss_zero = Column(self.column_index, "loss_zero", "INTEGER", Nullable.NULL)
        self.column_index += 1
        self.voltage = Column(self.column_index, "voltage", "NUMBER", Nullable.NULL)
        self.column_index += 1
        self.voltage_ohmic_part = Column(self.column_index, "voltage_ohmic_part", "NUMBER", Nullable.NULL)


class TableTransformerEndInfo(TableAssetInfo):
    connection_kind: Column = None
    emergency_s: Column = None
    end_number: Column = None
    insulation_u: Column = None
    phase_angle_clock: Column = None
    r: Column = None
    rated_s: Column = None
    rated_u: Column = None
    short_term_s: Column = None
    transformer_tank_info_mrid: Column = None

    def __init__(self):
        super(TableTransformerEndInfo, self).__init__()
        self.column_index += 1
        self.connection_kind = Column(self.column_index, "connection_kind", "TEXT", Nullable.NOT_NULL)
        self.column_index += 1
        self.emergency_s = Column(self.column_index, "emergency_s", "INTEGER", Nullable.NOT_NULL)
        self.column_index += 1
        self.end_number = Column(self.column_index, "end_number", "INTEGER", Nullable.NOT_NULL)
        self.column_index += 1
        self.insulation_u = Column(self.column_index, "insulation_u", "INTEGER", Nullable.NOT_NULL)
        self.column_index += 1
        self.phase_angle_clock = Column(self.column_index, "phase_angle_clock", "INTEGER", Nullable.NOT_NULL)
        self.column_index += 1
        self.r = Column(self.column_index, "r", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.rated_s = Column(self.column_index, "rated_s", "INTEGER", Nullable.NOT_NULL)
        self.column_index += 1
        self.rated_u = Column(self.column_index, "rated_u", "INTEGER", Nullable.NOT_NULL)
        self.column_index += 1
        self.short_term_s = Column(self.column_index, "short_term_s", "INTEGER", Nullable.NOT_NULL)
        self.column_index += 1
        self.transformer_tank_info_mrid = Column(self.column_index, "transformer_tank_info_mrid", "TEXT", Nullable.NULL)

    def name(self) -> str:
        return "transformer_end_info"

    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableTransformerEndInfo, self).non_unique_index_columns()
        cols.append([self.transformer_tank_info_mrid])
        return cols


class TableTransformerTankInfo(TableAssetInfo):
    power_transformer_info_mrid: Column = None

    def __init__(self):
        super(TableTransformerTankInfo, self).__init__()
        self.column_index += 1
        self.power_transformer_info_mrid = Column(self.column_index, "power_transformer_info_mrid", "TEXT", Nullable.NULL)

    def name(self) -> str:
        return "transformer_tank_info"

    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableTransformerTankInfo, self).non_unique_index_columns()
        cols.append([self.power_transformer_info_mrid])
        return cols


class TableWireInfo(TableAssetInfo):
    rated_current: Column = None
    material: Column = None

    def __init__(self):
        super(TableWireInfo, self).__init__()
        self.column_index += 1
        self.rated_current = Column(self.column_index, "rated_current", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.material = Column(self.column_index, "material", "TEXT", Nullable.NOT_NULL)


class TableCableInfo(TableWireInfo):

    def name(self) -> str:
        return "cable_info"


class TableOverheadWireInfo(TableWireInfo):

    def name(self) -> str:
        return "overhead_wire_info"
