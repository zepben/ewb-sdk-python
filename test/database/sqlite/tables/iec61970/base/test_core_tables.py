#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from test.database.sqlite.tables.table_test_utils import verify_column
from zepben.evolve import Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.core_tables import TableIdentifiedObjects, TableBaseVoltages, \
    TablePowerSystemResources,TableConnectivityNodes, TableEquipment, TableConductingEquipment, TableFeeders, TableGeographicalRegions, \
    TableNames, TableNameTypes, TableSites, TableSubGeographicalRegions, TableSubstations, TableTerminals


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
    assert t.unique_index_columns() == [[t.mrid]]
    assert t.non_unique_index_columns() == [[t.name_]]

def test_table_power_system_resources():
    t = TablePowerSystemResources()
    verify_column(t.location_mrid, 5, "location_mrid", "TEXT", Nullable.NULL)
    verify_column(t.num_controls, 6, "num_controls", "INTEGER", Nullable.NOT_NULL)
    assert t.unique_index_columns() == [[t.mrid]]
    assert t.non_unique_index_columns() == [[t.name_]]

def test_table_connectivity_nodes():
    t = TableConnectivityNodes()
    assert t.name() == "connectivity_nodes"
    assert t.unique_index_columns() == [[t.mrid]]
    assert t.non_unique_index_columns() == [[t.name_]]

def test_table_equipment():
    t = TableEquipment()
    verify_column(t.normally_in_service, 7, "normally_in_service", "BOOLEAN", Nullable.NONE)
    verify_column(t.in_service, 8, "in_service", "BOOLEAN", Nullable.NONE)
    assert t.unique_index_columns() == [[t.mrid]]
    assert t.non_unique_index_columns() == [[t.name_]]

def test_table_conducting_equipment():
    t = TableConductingEquipment()
    verify_column(t.base_voltage_mrid, 9, "base_voltage_mrid", "TEXT", Nullable.NULL)
    assert t.unique_index_columns() == [[t.mrid]]
    assert t.non_unique_index_columns() == [[t.name_]]

def test_table_feeders():
    t = TableFeeders()
    verify_column(t.normal_head_terminal_mrid, 7, "normal_head_terminal_mrid", "TEXT", Nullable.NULL)
    verify_column(t.normal_energizing_substation_mrid, 8, "normal_energizing_substation_mrid", "TEXT", Nullable.NULL)
    assert t.name() == "feeders"
    assert t.unique_index_columns() == [[t.mrid]]
    assert t.non_unique_index_columns() == [[t.name_], [t.normal_energizing_substation_mrid]]

def test_table_geographical_regions():
    t = TableGeographicalRegions()
    assert t.name() == "geographical_regions"
    assert t.unique_index_columns() == [[t.mrid]]
    assert t.non_unique_index_columns() == [[t.name_]]

def test_table_names():
    t = TableNames()
    verify_column(t.name_, 1, "name", "TEXT", Nullable.NOT_NULL)
    verify_column(t.identified_object_mrid, 2, "identified_object_mrid", "TEXT", Nullable.NOT_NULL)
    verify_column(t.name_type_name, 3, "name_type_name", "TEXT", Nullable.NOT_NULL)
    assert t.name() == "names"
    #assert t.unique_index_columns() == [[t.identified_object_mrid], [t.name_type_name], [t.name_]]
    assert t.non_unique_index_columns() == [[t.identified_object_mrid], [t.name_type_name], [t.name_]]

def test_table_name_types():
    t = TableNameTypes()
    verify_column(t.name_, 1, "name", "TEXT", Nullable.NOT_NULL)
    verify_column(t.description, 2, "description", "TEXT", Nullable.NULL)
    assert t.name() == "name_types"
    assert t.unique_index_columns() == [[t.name_]]

def test_table_table_sites():
    t = TableSites()
    assert t.name() == "sites"
    assert t.unique_index_columns() == [[t.mrid]]
    assert t.non_unique_index_columns() == [[t.name_]]

def test_table_sub_geographical_regions():
    t = TableSubGeographicalRegions()
    verify_column(t.geographical_region_mrid, 5, "geographical_region_mrid", "TEXT", Nullable.NULL)
    assert t.name() == "sub_geographical_regions"
    assert t.unique_index_columns() == [[t.mrid]]
    assert t.non_unique_index_columns() == [[t.name_],[t.geographical_region_mrid]]

def test_table_substations():
    t = TableSubstations()
    verify_column(t.sub_geographical_region_mrid, 7, "sub_geographical_region_mrid", "TEXT", Nullable.NULL)
    assert t.name() == "substations"
    assert t.unique_index_columns() == [[t.mrid]]
    assert t.non_unique_index_columns() == [[t.name_], [t.sub_geographical_region_mrid]]

def test_table_terminals():
    t = TableTerminals()
    verify_column(t.conducting_equipment_mrid, 5, "conducting_equipment_mrid", "TEXT", Nullable.NULL)
    verify_column(t.sequence_number, 6, "sequence_number", "INTEGER", Nullable.NOT_NULL)
    verify_column(t.connectivity_node_mrid, 7, "connectivity_node_mrid", "TEXT", Nullable.NULL)
    verify_column(t.phases, 8, "phases", "TEXT", Nullable.NOT_NULL)
    assert t.name() == "terminals"
    assert t.unique_index_columns() == [[t.mrid], [t.conducting_equipment_mrid, t.sequence_number]]
    assert t.non_unique_index_columns() == [[t.name_], [t.connectivity_node_mrid]]






