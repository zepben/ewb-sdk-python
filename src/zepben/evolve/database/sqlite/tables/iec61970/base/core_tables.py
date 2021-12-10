#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import List

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.sqlite_table import SqliteTable

__all__ = ["TablePowerSystemResources", "TableSites", "TableNames", "TableTerminals", "TableFeeders", "TableIdentifiedObjects", "TableSubstations",
           "TableAcDcTerminals", "TableEquipmentContainers", "TableEquipment", "TableConnectivityNodeContainers", "TableConductingEquipment",
           "TableBaseVoltages", "TableConnectivityNodes", "TableSubGeographicalRegions", "TableNameTypes", "TableEquipment", "TableGeographicalRegions"]


# noinspection PyAbstractClass
class TableIdentifiedObjects(SqliteTable):
    mrid: Column = None
    name_: Column = None
    description: Column = None
    num_diagram_objects: Column = None

    def __init__(self):
        self.mrid = self._create_column("mrid", "TEXT", Nullable.NOT_NULL)
        self.name_ = self._create_column("name", "TEXT", Nullable.NOT_NULL)
        self.description = self._create_column("description", "TEXT", Nullable.NOT_NULL)
        self.num_diagram_objects = self._create_column("num_diagram_objects", "INTEGER", Nullable.NOT_NULL)

    def unique_index_columns(self) -> List[List[Column]]:
        return [[self.mrid]]

    def non_unique_index_columns(self) -> List[List[Column]]:
        return [[self.name_]]


# noinspection PyAbstractClass
class TableAcDcTerminals(TableIdentifiedObjects):
    pass


class TableBaseVoltages(TableIdentifiedObjects):
    nominal_voltage: Column = None

    def __init__(self):
        super(TableBaseVoltages, self).__init__()
        self.nominal_voltage = self._create_column("nominal_voltage", "INTEGER", Nullable.NOT_NULL)

    def name(self) -> str:
        return "base_voltages"


# noinspection PyAbstractClass
class TablePowerSystemResources(TableIdentifiedObjects):
    location_mrid: Column = None
    num_controls: Column = None

    def __init__(self):
        super(TablePowerSystemResources, self).__init__()
        self.location_mrid = self._create_column("location_mrid", "TEXT", Nullable.NULL)
        self.num_controls = self._create_column("num_controls", "INTEGER", Nullable.NOT_NULL)


# noinspection PyAbstractClass
class TableConnectivityNodeContainers(TablePowerSystemResources):
    pass


class TableConnectivityNodes(TableIdentifiedObjects):

    def name(self) -> str:
        return "connectivity_nodes"


# noinspection PyAbstractClass
class TableEquipment(TablePowerSystemResources):
    normally_in_service: Column = None
    in_service: Column = None

    def __init__(self):
        super(TableEquipment, self).__init__()
        self.normally_in_service = self._create_column("normally_in_service", "BOOLEAN")
        self.in_service = self._create_column("in_service", "BOOLEAN")


# noinspection PyAbstractClass
class TableConductingEquipment(TableEquipment):
    base_voltage_mrid: Column = None

    def __init__(self):
        super(TableConductingEquipment, self).__init__()
        self.base_voltage_mrid = self._create_column("base_voltage_mrid", "TEXT", Nullable.NULL)


# noinspection PyAbstractClass
class TableEquipmentContainers(TableConnectivityNodeContainers):
    pass


class TableFeeders(TableEquipmentContainers):
    normal_head_terminal_mrid: Column = None
    normal_energizing_substation_mrid: Column = None

    def __init__(self):
        super(TableFeeders, self).__init__()
        self.normal_head_terminal_mrid = self._create_column("normal_head_terminal_mrid", "TEXT", Nullable.NULL)
        self.normal_energizing_substation_mrid = self._create_column("normal_energizing_substation_mrid", "TEXT", Nullable.NULL)

    def name(self) -> str:
        return "feeders"

    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableEquipmentContainers, self).non_unique_index_columns()
        cols.append([self.normal_energizing_substation_mrid])
        return cols


class TableGeographicalRegions(TableIdentifiedObjects):

    def name(self) -> str:
        return "geographical_regions"


class TableNames(SqliteTable):
    name_: Column = None
    identified_object_mrid: Column = None
    name_type_name: Column = None

    def __init__(self):
        super(TableNames, self).__init__()
        self.name_ = self._create_column("name", "TEXT", Nullable.NOT_NULL)
        self.identified_object_mrid = self._create_column("identified_object_mrid", "TEXT", Nullable.NOT_NULL)
        self.name_type_name = self._create_column("name_type_name", "TEXT", Nullable.NOT_NULL)

    def name(self) -> str:
        return "names"

    def unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableNames, self).unique_index_columns()
        cols.append([self.identified_object_mrid, self.name_type_name, self.name_])
        return cols

    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableNames, self).non_unique_index_columns()
        cols.append([self.identified_object_mrid])
        cols.append([self.name_type_name])
        cols.append([self.name_])
        return cols


class TableNameTypes(SqliteTable):
    name_: Column = None
    description: Column = None

    def __init__(self):
        super(TableNameTypes, self).__init__()
        self.name_ = self._create_column("name", "TEXT", Nullable.NOT_NULL)
        self.description = self._create_column("description", "TEXT", Nullable.NULL)

    def name(self) -> str:
        return "name_types"

    def unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableNameTypes, self).unique_index_columns()
        cols.append([self.name_])
        return cols


class TableSites(TableEquipmentContainers):

    def name(self) -> str:
        return "sites"


class TableSubGeographicalRegions(TableIdentifiedObjects):
    geographical_region_mrid: Column = None

    def __init__(self):
        super(TableSubGeographicalRegions, self).__init__()
        self.geographical_region_mrid = self._create_column("geographical_region_mrid", "TEXT", Nullable.NULL)

    def name(self) -> str:
        return "sub_geographical_regions"

    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableSubGeographicalRegions, self).non_unique_index_columns()
        cols.append([self.geographical_region_mrid])
        return cols


class TableSubstations(TableEquipmentContainers):
    sub_geographical_region_mrid: Column = None

    def __init__(self):
        super(TableSubstations, self).__init__()
        self.sub_geographical_region_mrid = self._create_column("sub_geographical_region_mrid", "TEXT", Nullable.NULL)

    def name(self) -> str:
        return "substations"

    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableSubstations, self).non_unique_index_columns()
        cols.append([self.sub_geographical_region_mrid])
        return cols


class TableTerminals(TableAcDcTerminals):
    conducting_equipment_mrid: Column = None
    sequence_number: Column = None
    connectivity_node_mrid: Column = None
    phases: Column = None

    def __init__(self):
        super(TableTerminals, self).__init__()
        self.conducting_equipment_mrid = self._create_column("conducting_equipment_mrid", "TEXT", Nullable.NULL)
        self.sequence_number = self._create_column("sequence_number", "INTEGER", Nullable.NOT_NULL)
        self.connectivity_node_mrid = self._create_column("connectivity_node_mrid", "TEXT", Nullable.NULL)
        self.phases = self._create_column("phases", "TEXT", Nullable.NOT_NULL)

    def name(self) -> str:
        return "terminals"

    def unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableTerminals, self).unique_index_columns()
        cols.append([self.conducting_equipment_mrid, self.sequence_number])
        return cols

    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableTerminals, self).non_unique_index_columns()
        cols.append([self.connectivity_node_mrid])
        return cols
