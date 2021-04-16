#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from test.database.sqlite.tables.table_test_utils import verify_column
from zepben.evolve import Nullable, TableTransformerEnds, TablePowerTransformerEnds, TablePowerTransformers, TableTapChangers, TableRatioTapChangers, \
    TableTransformerStarImpedance


def test_table_transformer_ends():
    t = TableTransformerEnds()
    verify_column(t.end_number, 5, "end_number", "INTEGER", Nullable.NOT_NULL)
    verify_column(t.terminal_mrid, 6, "terminal_mrid", "TEXT", Nullable.NULL)
    verify_column(t.base_voltage_mrid, 7, "base_voltage_mrid", "TEXT", Nullable.NULL)
    verify_column(t.grounded, 8, "grounded", "BOOLEAN", Nullable.NOT_NULL)
    verify_column(t.r_ground, 9, "r_ground", "NUMBER", Nullable.NOT_NULL)
    verify_column(t.x_ground, 10, "x_ground", "NUMBER", Nullable.NOT_NULL)
    verify_column(t.star_impedance_mrid, 11, "star_impedance_mrid", "TEXT", Nullable.NULL)
    assert t.non_unique_index_columns() == [*super(TableTransformerEnds, t).non_unique_index_columns(), [t.star_impedance_mrid]]


def test_table_power_transformer_ends():
    t = TablePowerTransformerEnds()
    verify_column(t.power_transformer_mrid, 12, "power_transformer_mrid", "TEXT", Nullable.NULL)
    verify_column(t.connection_kind, 13, "connection_kind", "TEXT", Nullable.NOT_NULL)
    verify_column(t.phase_angle_clock, 14, "phase_angle_clock", "INTEGER", Nullable.NOT_NULL)
    verify_column(t.b, 15, "b", "NUMBER", Nullable.NOT_NULL)
    verify_column(t.b0, 16, "b0", "NUMBER", Nullable.NOT_NULL)
    verify_column(t.g, 17, "g", "NUMBER", Nullable.NOT_NULL)
    verify_column(t.g0, 18, "g0", "NUMBER", Nullable.NOT_NULL)
    verify_column(t.r, 19, "r", "NUMBER", Nullable.NULL)
    verify_column(t.r0, 20, "r0", "NUMBER", Nullable.NULL)
    verify_column(t.rated_s, 21, "rated_s", "INTEGER", Nullable.NOT_NULL)
    verify_column(t.rated_u, 22, "rated_u", "INTEGER", Nullable.NOT_NULL)
    verify_column(t.x, 23, "x", "NUMBER", Nullable.NULL)
    verify_column(t.x0, 24, "x0", "NUMBER", Nullable.NULL)
    assert t.unique_index_columns() == [*super(TablePowerTransformerEnds, t).unique_index_columns(), [t.power_transformer_mrid, t.end_number]]
    assert t.non_unique_index_columns() == [*super(TablePowerTransformerEnds, t).non_unique_index_columns(), [t.power_transformer_mrid]]
    assert t.name() == "power_transformer_ends"


def test_table_power_transformers():
    t = TablePowerTransformers()
    verify_column(t.vector_group, 10, "vector_group", "TEXT", Nullable.NOT_NULL)
    verify_column(t.transformer_utilisation, 11, "transformer_utilisation", "NUMBER", Nullable.NULL)
    verify_column(t.power_transformer_info_mrid, 12, "power_transformer_info_mrid", "TEXT", Nullable.NULL)
    assert t.name() == "power_transformers"


def test_table_tap_changers():
    t = TableTapChangers()
    verify_column(t.control_enabled, 7, "control_enabled", "BOOLEAN", Nullable.NOT_NULL)
    verify_column(t.high_step, 8, "high_step", "INTEGER", Nullable.NOT_NULL)
    verify_column(t.low_step, 9, "low_step", "INTEGER", Nullable.NOT_NULL)
    verify_column(t.neutral_step, 10, "neutral_step", "INTEGER", Nullable.NOT_NULL)
    verify_column(t.neutral_u, 11, "neutral_u", "INTEGER", Nullable.NOT_NULL)
    verify_column(t.normal_step, 12, "normal_step", "INTEGER", Nullable.NOT_NULL)
    verify_column(t.step, 13, "step", "NUMBER", Nullable.NOT_NULL)


def test_table_ratio_tap_changers():
    t = TableRatioTapChangers()
    verify_column(t.transformer_end_mrid, 14, "transformer_end_mrid", "TEXT", Nullable.NULL)
    verify_column(t.step_voltage_increment, 15, "step_voltage_increment", "NUMBER", Nullable.NOT_NULL)
    assert t.unique_index_columns() == [*super(TableRatioTapChangers, t).unique_index_columns(), [t.transformer_end_mrid]]
    assert t.name() == "ratio_tap_changers"


def test_table_transformer_star_impedance():
    t = TableTransformerStarImpedance()
    verify_column(t.r, 5, "R", "NUMBER", Nullable.NULL)
    verify_column(t.r0, 6, "R0", "NUMBER", Nullable.NULL)
    verify_column(t.x, 7, "X", "NUMBER", Nullable.NULL)
    verify_column(t.x0, 8, "X0", "NUMBER", Nullable.NULL)
    verify_column(t.transformer_end_info_mrid, 9, "transformer_end_info_mrid", "TEXT", Nullable.NULL)
    assert t.unique_index_columns() == [*super(TableTransformerStarImpedance, t).unique_index_columns(), [t.transformer_end_info_mrid]]
    assert t.name() == "transformer_star_impedance"
