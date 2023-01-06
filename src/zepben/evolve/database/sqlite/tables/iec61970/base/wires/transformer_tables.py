#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.core_tables import TableIdentifiedObjects, TableConductingEquipment, TablePowerSystemResources

__all__ = ["TableTransformerEnds", "TablePowerTransformerEnds", "TablePowerTransformers", "TableTapChangers", "TableRatioTapChangers",
           "TableTransformerStarImpedance"]


# noinspection PyAbstractClass
class TableTransformerEnds(TableIdentifiedObjects):
    end_number: Column
    terminal_mrid: Column
    base_voltage_mrid: Column
    grounded: Column
    r_ground: Column
    x_ground: Column
    star_impedance_mrid: Column

    def __init__(self):
        super(TableTransformerEnds, self).__init__()
        self.end_number = self._create_column("end_number", "INTEGER", Nullable.NOT_NULL)
        self.terminal_mrid = self._create_column("terminal_mrid", "TEXT", Nullable.NULL)
        self.base_voltage_mrid = self._create_column("base_voltage_mrid", "TEXT", Nullable.NULL)
        self.grounded = self._create_column("grounded", "BOOLEAN", Nullable.NOT_NULL)
        self.r_ground = self._create_column("r_ground", "NUMBER", Nullable.NULL)
        self.x_ground = self._create_column("x_ground", "NUMBER", Nullable.NULL)
        self.star_impedance_mrid = self._create_column("star_impedance_mrid", "TEXT", Nullable.NULL)

    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableTransformerEnds, self).non_unique_index_columns()
        cols.append([self.star_impedance_mrid])
        return cols


class TablePowerTransformerEnds(TableTransformerEnds):
    power_transformer_mrid: Column
    connection_kind: Column
    phase_angle_clock: Column
    b: Column
    b0: Column
    g: Column
    g0: Column
    r: Column
    r0: Column
    rated_s: Column
    rated_u: Column
    x: Column
    x0: Column

    def __init__(self):
        super(TablePowerTransformerEnds, self).__init__()
        self.power_transformer_mrid = self._create_column("power_transformer_mrid", "TEXT", Nullable.NULL)
        self.connection_kind = self._create_column("connection_kind", "TEXT", Nullable.NOT_NULL)
        self.phase_angle_clock = self._create_column("phase_angle_clock", "INTEGER", Nullable.NULL)
        self.b = self._create_column("b", "NUMBER", Nullable.NULL)
        self.b0 = self._create_column("b0", "NUMBER", Nullable.NULL)
        self.g = self._create_column("g", "NUMBER", Nullable.NULL)
        self.g0 = self._create_column("g0", "NUMBER", Nullable.NULL)
        self.r = self._create_column("r", "NUMBER", Nullable.NULL)
        self.r0 = self._create_column("r0", "NUMBER", Nullable.NULL)
        self.rated_s = self._create_column("rated_s", "INTEGER", Nullable.NULL)
        self.rated_u = self._create_column("rated_u", "INTEGER", Nullable.NULL)
        self.x = self._create_column("x", "NUMBER", Nullable.NULL)
        self.x0 = self._create_column("x0", "NUMBER", Nullable.NULL)

    def name(self) -> str:
        return "power_transformer_ends"

    def unique_index_columns(self) -> List[List[Column]]:
        cols = super(TablePowerTransformerEnds, self).unique_index_columns()
        cols.append([self.power_transformer_mrid, self.end_number])
        return cols

    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TablePowerTransformerEnds, self).non_unique_index_columns()
        cols.append([self.power_transformer_mrid])
        return cols


class TablePowerTransformers(TableConductingEquipment):
    vector_group: Column
    transformer_utilisation: Column
    construction_kind: Column
    function: Column
    power_transformer_info_mrid: Column

    def __init__(self):
        super(TablePowerTransformers, self).__init__()
        self.vector_group = self._create_column("vector_group", "TEXT", Nullable.NOT_NULL)
        self.transformer_utilisation = self._create_column("transformer_utilisation", "NUMBER", Nullable.NULL)
        self.construction_kind = self._create_column("construction_kind", "TEXT", Nullable.NOT_NULL)
        self.function = self._create_column("function", "TEXT", Nullable.NOT_NULL)
        self.power_transformer_info_mrid = self._create_column("power_transformer_info_mrid", "TEXT", Nullable.NULL)

    def name(self) -> str:
        return "power_transformers"


# noinspection PyAbstractClass
class TableTapChangers(TablePowerSystemResources):
    control_enabled: Column
    high_step: Column
    low_step: Column
    neutral_step: Column
    neutral_u: Column
    normal_step: Column
    step: Column

    def __init__(self):
        super(TableTapChangers, self).__init__()
        self.control_enabled = self._create_column("control_enabled", "BOOLEAN", Nullable.NOT_NULL)
        self.high_step = self._create_column("high_step", "INTEGER", Nullable.NULL)
        self.low_step = self._create_column("low_step", "INTEGER", Nullable.NULL)
        self.neutral_step = self._create_column("neutral_step", "INTEGER", Nullable.NULL)
        self.neutral_u = self._create_column("neutral_u", "INTEGER", Nullable.NULL)
        self.normal_step = self._create_column("normal_step", "INTEGER", Nullable.NULL)
        self.step = self._create_column("step", "NUMBER", Nullable.NULL)


class TableRatioTapChangers(TableTapChangers):
    transformer_end_mrid: Column
    step_voltage_increment: Column

    def __init__(self):
        super(TableRatioTapChangers, self).__init__()
        self.transformer_end_mrid = self._create_column("transformer_end_mrid", "TEXT", Nullable.NULL)
        self.step_voltage_increment = self._create_column("step_voltage_increment", "NUMBER", Nullable.NULL)

    def name(self) -> str:
        return "ratio_tap_changers"

    def unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableRatioTapChangers, self).unique_index_columns()
        cols.append([self.transformer_end_mrid])
        return cols


class TableTransformerStarImpedance(TableIdentifiedObjects):
    r: Column
    r0: Column
    x: Column
    x0: Column
    transformer_end_info_mrid: Column

    def __init__(self):
        super(TableTransformerStarImpedance, self).__init__()
        # Note r, r0, x, x0 use nullable number types.
        self.r = self._create_column("R", "NUMBER", Nullable.NULL)
        self.r0 = self._create_column("R0", "NUMBER", Nullable.NULL)
        self.x = self._create_column("X", "NUMBER", Nullable.NULL)
        self.x0 = self._create_column("X0", "NUMBER", Nullable.NULL)
        self.transformer_end_info_mrid = self._create_column("transformer_end_info_mrid", "TEXT", Nullable.NULL)

    def unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableTransformerStarImpedance, self).unique_index_columns()
        cols.append([self.transformer_end_info_mrid])
        return cols

    def name(self) -> str:
        return "transformer_star_impedance"
