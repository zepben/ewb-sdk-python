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
    end_number: Column = None
    terminal_mrid: Column = None
    base_voltage_mrid: Column = None
    grounded: Column = None
    r_ground: Column = None
    x_ground: Column = None
    star_impedance_mrid: Column = None

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
    power_transformer_mrid: Column = None
    connection_kind: Column = None
    phase_angle_clock: Column = None
    b: Column = None
    b0: Column = None
    g: Column = None
    g0: Column = None
    r: Column = None
    r0: Column = None
    rated_s: Column = None
    rated_u: Column = None
    x: Column = None
    x0: Column = None

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
    vector_group: Column = None
    transformer_utilisation: Column = None
    construction_kind: Column = None
    function: Column = None
    power_transformer_info_mrid: Column = None

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
    control_enabled: Column = None
    high_step: Column = None
    low_step: Column = None
    neutral_step: Column = None
    neutral_u: Column = None
    normal_step: Column = None
    step: Column = None

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
    transformer_end_mrid: Column = None
    step_voltage_increment: Column = None

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
    r: Column = None
    r0: Column = None
    x: Column = None
    x0: Column = None
    transformer_end_info_mrid: Column = None

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
