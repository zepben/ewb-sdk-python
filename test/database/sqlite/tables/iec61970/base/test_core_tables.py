#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from test.database.sqlite.tables.table_test_utils import verify_column
from zepben.evolve import Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.core_tables import TableIdentifiedObjects, TableBaseVoltages, TablePowerSystemResources


def test_table_identified_objects():
    t = TableIdentifiedObjects()
    verify_column(t.mrid, 1, "mrid", "TEXT", Nullable.NOT_NULL)
    verify_column(t.name_, 2, "name", "TEXT", Nullable.NOT_NULL)
    verify_column(t.description, 3, "description", "TEXT", Nullable.NOT_NULL)
    verify_column(t.num_diagram_objects, 4, "num_diagram_objects", "INTEGER", Nullable.NOT_NULL)

    assert t.unique_index_columns() == [[t.mrid]]
    assert t.non_unique_index_columns() == [[t.name_]]


def test_table_base_voltages():
    t = TableBaseVoltages()
    verify_column(t.nominal_voltage, 5, "nominal_voltage", "INTEGER", Nullable.NOT_NULL)
    assert t.name() == "base_voltages"


def test_table_power_system_resources():
    t = TablePowerSystemResources()
    verify_column(t.location_mrid, 5, "location_mrid", "TEXT", Nullable.NULL)
    verify_column(t.num_controls, 6, "num_controls", "INTEGER", Nullable.NOT_NULL)
