#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from test.database.sqlite.tables.table_test_utils import verify_column
from zepben.evolve import Nullable, TablePowerTransformerInfo, TableTransformerEndInfo, TableTransformerTankInfo, TableWireInfo, TableCableInfo, \
    TableOverheadWireInfo


def test_table_power_transformer_info():
    t = TablePowerTransformerInfo()
    assert t.name() == "power_transformer_info"


def test_table_transformer_end_info():
    t = TableTransformerEndInfo()
    verify_column(t.connection_kind, 5, "connection_kind", "TEXT", Nullable.NOT_NULL)
    verify_column(t.emergency_s, 6, "emergency_s", "INTEGER", Nullable.NOT_NULL)
    verify_column(t.end_number, 7, "end_number", "INTEGER", Nullable.NOT_NULL)
    verify_column(t.insulation_u, 8, "insulation_u", "INTEGER", Nullable.NOT_NULL)
    verify_column(t.phase_angle_clock, 9, "phase_angle_clock", "INTEGER", Nullable.NOT_NULL)
    verify_column(t.r, 10, "r", "NUMBER", Nullable.NOT_NULL)
    verify_column(t.rated_s, 11, "rated_s", "INTEGER", Nullable.NOT_NULL)
    verify_column(t.rated_u, 12, "rated_u", "INTEGER", Nullable.NOT_NULL)
    verify_column(t.short_term_s, 13, "short_term_s", "INTEGER", Nullable.NOT_NULL)
    verify_column(t.transformer_tank_info_mrid, 14, "transformer_tank_info_mrid", "TEXT", Nullable.NULL)
    assert t.non_unique_index_columns() == [*super(TableTransformerEndInfo, t).non_unique_index_columns(), [t.transformer_tank_info_mrid]]
    assert t.name() == "transformer_end_info"


def test_table_transformer_tank_info():
    t = TableTransformerTankInfo()
    verify_column(t.power_transformer_info_mrid, 5, "power_transformer_info_mrid", "TEXT", Nullable.NULL)
    assert t.non_unique_index_columns() == [*super(TableTransformerTankInfo, t).non_unique_index_columns(), [t.power_transformer_info_mrid]]
    assert t.name() == "transformer_tank_info"


def test_table_wire_info():
    t = TableWireInfo()
    verify_column(t.rated_current, 5, "rated_current", "NUMBER", Nullable.NOT_NULL)
    verify_column(t.material, 6, "material", "TEXT", Nullable.NOT_NULL)


def test_table_cable_info():
    t = TableCableInfo()
    assert t.name() == "cable_info"


def test_table_overhead_wire_info():
    t = TableOverheadWireInfo()
    assert t.name() == "overhead_wire_info"
