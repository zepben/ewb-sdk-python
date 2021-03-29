#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import List

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.core_tables import TableIdentifiedObjects, TableConductingEquipment, TablePowerSystemResources


class TableTransformerEnds(TableIdentifiedObjects):
    end_number: Column = None
    terminal_mrid: Column = None
    base_voltage_mrid: Column = None
    grounded: Column = None
    r_ground: Column = None
    x_ground: Column = None
    star_impedance_mrid: Column = None

    def __init__(self):
        super().__init__()
        self.column_index += 1
        self.end_number = Column(self.column_index, "end_number", "INTEGER", Nullable.NOT_NULL)
        self.column_index += 1
        self.terminal_mrid = Column(self.column_index, "terminal_mrid", "TEXT", Nullable.NULL)
        self.column_index += 1
        self.base_voltage_mrid = Column(self.column_index, "base_voltage_mrid", "TEXT", Nullable.NULL)
        self.column_index += 1
        self.grounded = Column(self.column_index, "phase", "BOOLEAN", Nullable.NOT_NULL)
        self.column_index += 1
        self.r_ground = Column(self.column_index, "r_ground", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.x_ground = Column(self.column_index, "x_ground", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.star_impedance_mrid = Column(self.column_index, "star_impedance_mrid", "TEXT", Nullable.NULL)

    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super().non_unique_index_columns()
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
        super().__init__()
        self.column_index += 1
        self.power_transformer_mrid = Column(self.column_index, "power_transformer_mrid", "TEXT", Nullable.NULL)
        self.column_index += 1
        self.connection_kind = Column(self.column_index, "connection_kind", "TEXT", Nullable.NOT_NULL)
        self.column_index += 1
        self.phase_angle_clock = Column(self.column_index, "phase_angle_clock", "INTEGER", Nullable.NOT_NULL)
        self.column_index += 1
        self.b = Column(self.column_index, "b", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.b0 = Column(self.column_index, "b0", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.g = Column(self.column_index, "g", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.g0 = Column(self.column_index, "g0", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.r = Column(self.column_index, "r", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.r0 = Column(self.column_index, "r0", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.rated_s = Column(self.column_index, "rated_s", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.rated_u = Column(self.column_index, "rated_u", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.x = Column(self.column_index, "x", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.x0 = Column(self.column_index, "x0", "NUMBER", Nullable.NOT_NULL)

    def name(self) -> str:
        return "power_transformer_ends"

    def unique_index_columns(self) -> List[List[Column]]:
        cols = super().unique_index_columns()
        cols.append([self.power_transformer_mrid, self.end_number])
        return cols

    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super().non_unique_index_columns()
        cols.append([self.power_transformer_mrid])
        return cols


class TablePowerTransformers(TableConductingEquipment):
    vector_group: Column = None
    transformer_utilisation: Column = None
    power_transformer_info_mrid: Column = None

    def __init__(self):
        super().__init__()
        self.column_index += 1
        self.vector_group = Column(self.column_index, "vector_group", "TEXT", Nullable.NOT_NULL)
        self.column_index += 1
        self.transformer_utilisation = Column(self.column_index, "transformer_utilisation", "NUMBER", Nullable.NULL)
        self.column_index += 1
        self.power_transformer_info_mrid = Column(self.column_index, "power_transformer_info_mrid", "TEXT", Nullable.NULL)

    def name(self) -> str:
        return "power_transformers"


class TableTapChangers(TablePowerSystemResources):
    control_enabled: Column = None
    high_step: Column = None
    low_step: Column = None
    neutral_step: Column = None
    neutral_u: Column = None
    normal_step: Column = None
    step: Column = None

    def __init__(self):
        super().__init__()
        self.column_index += 1
        self.control_enabled = Column(self.column_index, "control_enabled", "BOOLEAN", Nullable.NOT_NULL)
        self.column_index += 1
        self.high_step = Column(self.column_index, "high_step", "INTEGER", Nullable.NOT_NULL)
        self.column_index += 1
        self.low_step = Column(self.column_index, "low_step", "INTEGER", Nullable.NOT_NULL)
        self.column_index += 1
        self.neutral_step = Column(self.column_index, "neutral_step", "INTEGER", Nullable.NOT_NULL)
        self.column_index += 1
        self.neutral_u = Column(self.column_index, "neutral_u", "INTEGER", Nullable.NOT_NULL)
        self.column_index += 1
        self.normal_step = Column(self.column_index, "normal_step", "INTEGER", Nullable.NOT_NULL)
        self.column_index += 1
        self.step = Column(self.column_index, "step", "NUMBER", Nullable.NOT_NULL)


class TableRatioTapChangers(TableTapChangers):
    transformer_end_mrid: Column = None
    step_voltage_increment: Column = None

    def __init__(self):
        super().__init__()
        self.column_index += 1
        self.transformer_end_mrid = Column(self.column_index, "transformer_end_mrid", "TEXT", Nullable.NULL)
        self.column_index += 1
        self.step_voltage_increment = Column(self.column_index, "step_voltage_increment", "NUMBER", Nullable.NOT_NULL)

    def name(self) -> str:
        return "ratio_tap_changers"

    def unique_index_columns(self) -> List[List[Column]]:
        cols = super().unique_index_columns()
        cols.append([self.transformer_end_mrid])
        return cols


class TableTransformerStarImpedance(TableIdentifiedObjects):
    r: Column = None
    r0: Column = None
    x: Column = None
    x0: Column = None
    transformer_end_info_mrid: Column = None

    def __init__(self):
        super().__init__()
        # Note r, r0, x, x0 use nullable number types.
        self.column_index += 1
        self.r = Column(self.column_index, "r", "NUMBER", Nullable.NULL)
        self.column_index += 1
        self.r0 = Column(self.column_index, "r0", "NUMBER", Nullable.NULL)
        self.column_index += 1
        self.x = Column(self.column_index, "x", "NUMBER", Nullable.NULL)
        self.column_index += 1
        self.x0 = Column(self.column_index, "x0", "NUMBER", Nullable.NULL)
        self.column_index += 1
        self.transformer_end_info_mrid = Column(self.column_index, "transformer_end_info_mrid", "TEXT", Nullable.NULL)

    def unique_index_columns(self) -> List[List[Column]]:
        cols = super().unique_index_columns()
        cols.append([self.transformer_end_info_mrid])
        return cols
