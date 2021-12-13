#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import List

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61968.asset_tables import TableAssetInfo

__all__ = ["TablePowerTransformerInfo", "TableTransformerEndInfo", "TableTransformerTankInfo", "TableWireInfo", "TableCableInfo", "TableAssetInfo",
           "TableOverheadWireInfo", "TableNoLoadTests", "TableOpenCircuitTests", "TableShortCircuitTests", "TableTransformerTest", "TableShuntCompensatorInfo"]


# noinspection PyAbstractClass
class TableTransformerTest(TableAssetInfo):
    base_power: Column = None
    temperature: Column = None

    def __init__(self):
        super(TableTransformerTest, self).__init__()
        self.base_power = self._create_column("base_power", "INTEGER", Nullable.NULL)
        self.temperature = self._create_column("temperature", "NUMBER", Nullable.NULL)


class TableNoLoadTests(TableTransformerTest):
    energised_end_voltage: Column = None
    exciting_current: Column = None
    exciting_current_zero: Column = None
    loss: Column = None
    loss_zero: Column = None

    def name(self) -> str:
        return "no_load_tests"

    def __init__(self):
        super(TableNoLoadTests, self).__init__()
        self.energised_end_voltage = self._create_column("energised_end_voltage", "INTEGER", Nullable.NULL)
        self.exciting_current = self._create_column("exciting_current", "NUMBER", Nullable.NULL)
        self.exciting_current_zero = self._create_column("exciting_current_zero", "NUMBER", Nullable.NULL)
        self.loss = self._create_column("loss", "NUMBER", Nullable.NULL)
        self.loss_zero = self._create_column("loss_zero", "INTEGER", Nullable.NULL)


class TableOpenCircuitTests(TableTransformerTest):
    energised_end_step: Column = None
    energised_end_voltage: Column = None
    open_end_step: Column = None
    open_end_voltage: Column = None
    phase_shift: Column = None

    def name(self) -> str:
        return "open_circuit_tests"

    def __init__(self):
        super(TableOpenCircuitTests, self).__init__()
        self.energised_end_voltage = self._create_column("energised_end_step", "INTEGER", Nullable.NULL)
        self.energised_end_step = self._create_column("energised_end_voltage", "INTEGER", Nullable.NULL)
        self.open_end_step = self._create_column("open_end_step", "INTEGER", Nullable.NULL)
        self.open_end_voltage = self._create_column("open_end_voltage", "INTEGER", Nullable.NULL)
        self.phase_shift = self._create_column("phase_shift", "NUMBER", Nullable.NULL)


class TablePowerTransformerInfo(TableAssetInfo):

    def name(self) -> str:
        return "power_transformer_info"


class TableShortCircuitTests(TableTransformerTest):
    current: Column = None
    energised_end_step: Column = None
    grounded_end_step: Column = None
    leakage_impedance: Column = None
    leakage_impedance_zero: Column = None
    loss: Column = None
    loss_zero: Column = None
    power: Column = None
    voltage: Column = None
    voltage_ohmic_part: Column = None

    def name(self) -> str:
        return "short_circuit_tests"

    def __init__(self):
        super(TableShortCircuitTests, self).__init__()
        self.current = self._create_column("current", "NUMBER", Nullable.NULL)
        self.energised_end_step = self._create_column("energised_end_step", "INTEGER", Nullable.NULL)
        self.grounded_end_step = self._create_column("grounded_end_step", "INTEGER", Nullable.NULL)
        self.leakage_impedance = self._create_column("leakage_impedance", "NUMBER", Nullable.NULL)
        self.leakage_impedance_zero = self._create_column("leakage_impedance_zero", "NUMBER", Nullable.NULL)
        self.loss = self._create_column("loss", "INTEGER", Nullable.NULL)
        self.loss_zero = self._create_column("loss_zero", "INTEGER", Nullable.NULL)
        self.power = self._create_column("power", "NUMBER", Nullable.NULL)
        self.voltage = self._create_column("voltage", "NUMBER", Nullable.NULL)
        self.voltage_ohmic_part = self._create_column("voltage_ohmic_part", "NUMBER", Nullable.NULL)


class TableShuntCompensatorInfo(TableAssetInfo):
    max_power_loss: Column = None
    rated_current: Column = None
    rated_reactive_power: Column = None
    rated_voltage: Column = None

    def __init__(self):
        super(TableShuntCompensatorInfo, self).__init__()
        self.max_power_loss = self._create_column("max_power_loss", "INTEGER", Nullable.NULL)
        self.rated_current = self._create_column("rated_current", "INTEGER", Nullable.NULL)
        self.rated_reactive_power = self._create_column("rated_reactive_power", "INTEGER", Nullable.NULL)
        self.rated_voltage = self._create_column("rated_voltage", "INTEGER", Nullable.NULL)

    def name(self) -> str:
        return "shunt_compensator_info"


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
    energised_end_no_load_tests: Column = None
    energised_end_short_circuit_tests: Column = None
    grounded_end_short_circuit_tests: Column = None
    open_end_open_circuit_tests: Column = None
    energised_end_open_circuit_tests: Column = None

    def __init__(self):
        super(TableTransformerEndInfo, self).__init__()
        self.connection_kind = self._create_column("connection_kind", "TEXT", Nullable.NOT_NULL)
        self.emergency_s = self._create_column("emergency_s", "INTEGER", Nullable.NULL)
        self.end_number = self._create_column("end_number", "INTEGER", Nullable.NOT_NULL)
        self.insulation_u = self._create_column("insulation_u", "INTEGER", Nullable.NULL)
        self.phase_angle_clock = self._create_column("phase_angle_clock", "INTEGER", Nullable.NULL)
        self.r = self._create_column("r", "NUMBER", Nullable.NULL)
        self.rated_s = self._create_column("rated_s", "INTEGER", Nullable.NULL)
        self.rated_u = self._create_column("rated_u", "INTEGER", Nullable.NULL)
        self.short_term_s = self._create_column("short_term_s", "INTEGER", Nullable.NULL)
        self.transformer_tank_info_mrid = self._create_column("transformer_tank_info_mrid", "TEXT", Nullable.NULL)
        self.energised_end_no_load_tests = self._create_column("energised_end_no_load_tests", "TEST", Nullable.NULL)
        self.energised_end_short_circuit_tests = self._create_column("energised_end_short_circuit_tests", "TEST", Nullable.NULL)
        self.grounded_end_short_circuit_tests = self._create_column("grounded_end_short_circuit_tests", "TEST", Nullable.NULL)
        self.open_end_open_circuit_tests = self._create_column("open_end_open_circuit_tests", "TEST", Nullable.NULL)
        self.energised_end_open_circuit_tests = self._create_column("energised_end_open_circuit_tests", "TEST", Nullable.NULL)

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
        self.power_transformer_info_mrid = self._create_column("power_transformer_info_mrid", "TEXT", Nullable.NULL)

    def name(self) -> str:
        return "transformer_tank_info"

    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableTransformerTankInfo, self).non_unique_index_columns()
        cols.append([self.power_transformer_info_mrid])
        return cols


# noinspection PyAbstractClass
class TableWireInfo(TableAssetInfo):
    rated_current: Column = None
    material: Column = None

    def __init__(self):
        super(TableWireInfo, self).__init__()
        self.rated_current = self._create_column("rated_current", "NUMBER", Nullable.NULL)
        self.material = self._create_column("material", "TEXT", Nullable.NOT_NULL)


class TableCableInfo(TableWireInfo):

    def name(self) -> str:
        return "cable_info"


class TableOverheadWireInfo(TableWireInfo):

    def name(self) -> str:
        return "overhead_wire_info"
