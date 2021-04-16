#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from test.database.sqlite.tables.table_test_utils import verify_column
from zepben.evolve import TableMeasurements, Nullable, TableAccumulators, TableAnalogs, TableDiscretes


def test_table_measurements():
    t = TableMeasurements()
    verify_column(t.power_system_resource_mrid, 5, "power_system_resource_mrid", "TEXT", Nullable.NULL)
    verify_column(t.remote_source_mrid, 6, "remote_source_mrid", "TEXT", Nullable.NULL)
    verify_column(t.terminal_mrid, 7, "terminal_mrid", "TEXT", Nullable.NULL)
    verify_column(t.phases, 8, "phases", "TEXT", Nullable.NOT_NULL)
    verify_column(t.unit_symbol, 9, "unit_symbol", "TEXT", Nullable.NOT_NULL)
    assert t.non_unique_index_columns() == [[t.name_], [t.power_system_resource_mrid], [t.remote_source_mrid], [t.terminal_mrid]]


def test_table_accumulators():
    t = TableAccumulators()
    assert t.name() == "accumulators"


def test_table_analogs():
    t = TableAnalogs()
    verify_column(t.positive_flow_in, 10, "positive_flow_in", "BOOLEAN", Nullable.NOT_NULL)
    assert t.name() == "analogs"


def test_table_discretes():
    t = TableDiscretes()
    assert t.name() == "discretes"
