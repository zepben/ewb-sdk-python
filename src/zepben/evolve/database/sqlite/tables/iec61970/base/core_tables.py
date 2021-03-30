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
           "TableBaseVoltages", "TableConnectivityNodes", "TableSubGeographicalRegions", "TableNameTypes", "TableEquipment"]


class TableIdentifiedObjects(SqliteTable):
    mrid: Column = None
    name_: Column = None
    description: Column = None
    num_diagram_objects: Column = None

    def __init__(self):
        self.column_index += 1
        self.mrid = Column(self.column_index, "mrid", "TEXT", Nullable.NOT_NULL)
        self.column_index += 1
        self.name_ = Column(self.column_index, "name", "TEXT", Nullable.NOT_NULL)
        self.column_index += 1
        self.description = Column(self.column_index, "description", "TEXT", Nullable.NOT_NULL)
        self.column_index += 1
        self.num_diagram_objects = Column(self.column_index, "num_diagram_objects", "INTEGER", Nullable.NOT_NULL)

    def unique_index_columns(self) -> List[List[Column]]:
        return [[self.mrid]]

    def non_unique_index_columns(self) -> List[List[Column]]:
        return [[self.name_]]


class TableAcDcTerminals(TableIdentifiedObjects):
    pass


class TableBaseVoltages(TableIdentifiedObjects):
    nominal_voltage: Column = None

    def __init__(self):
        super().__init__()
        self.column_index += 1
        self.nominal_voltage = Column(self.column_index, "nominal_voltage", "INTEGER", Nullable.NOT_NULL)

    def name(self) -> str:
        return "base_voltages"


class TablePowerSystemResources(TableIdentifiedObjects):
    location_mrid: Column = None
    num_controls: Column = None

    def __init__(self):
        super(TablePowerSystemResources, self).__init__()
        self.column_index += 1
        self.location_mrid = Column(self.column_index, "location_mrid", "TEXT", Nullable.NULL)
        self.column_index += 1
        self.num_controls = Column(self.column_index, "num_controls", "INTEGER", Nullable.NOT_NULL)


class TableConnectivityNodeContainers(TablePowerSystemResources):
    pass


class TableConnectivityNodes(TableIdentifiedObjects):

    def name(self) -> str:
        return "connectivity_nodes"


class TableEquipment(TablePowerSystemResources):
    normally_in_service: Column = None
    in_service: Column = None

    def __init__(self):
        super().__init__()
        self.column_index += 1
        self.normally_in_service = Column(self.column_index, "normally_in_service", "BOOLEAN")
        self.column_index += 1
        self.in_service = Column(self.column_index, "in_service", "BOOLEAN")


class TableConductingEquipment(TableEquipment):
    base_voltage_mrid: Column = None

    def __init__(self):
        super().__init__()
        self.column_index += 1
        self.base_voltage_mrid = Column(self.column_index, "base_voltage_mrid", "TEXT", Nullable.NULL)


class TableEquipmentContainers(TableConnectivityNodeContainers):
    pass


class TableFeeders(TableEquipmentContainers):
    normal_head_terminal_mrid: Column = None
    normal_energizing_substation_mrid: Column = None

    def __init__(self):
        super().__init__()
        self.column_index += 1
        self.normal_head_terminal_mrid = Column(self.column_index, "normal_head_terminal_mrid", "TEXT", Nullable.NULL)
        self.column_index += 1
        self.normal_energizing_substation_mrid = Column(self.column_index, "normal_energizing_substation_mrid", "TEXT", Nullable.NULL)

    def name(self) -> str:
        return "feeders"

    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super().non_unique_index_columns()
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
        super().__init__()
        self.column_index += 1
        self.name_ = Column(self.column_index, "name", "TEXT", Nullable.NOT_NULL)
        self.column_index += 1
        self.identified_object_mrid = Column(self.column_index, "identified_object_mrid", "TEXT", Nullable.NOT_NULL)
        self.column_index += 1
        self.name_type_name = Column(self.column_index, "name_type_name", "TEXT", Nullable.NOT_NULL)

    def name(self) -> str:
        return "names"

    def unique_index_columns(self) -> List[List[Column]]:
        cols = super().unique_index_columns()
        cols.append([self.identified_object_mrid, self.name_type_name, self.name])
        return cols

    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super().non_unique_index_columns()
        cols.append([self.identified_object_mrid])
        cols.append([self.name_type_name])
        cols.append([self.name])
        return cols


class TableNameTypes(SqliteTable):
    name_: Column = None
    description: Column = None

    def __init__(self):
        super().__init__()
        self.column_index += 1
        self.name_ = Column(self.column_index, "name", "TEXT", Nullable.NOT_NULL)
        self.column_index += 1
        self.description = Column(self.column_index, "description", "TEXT", Nullable.NULL)

    def name(self) -> str:
        return "name_types"

    def unique_index_columns(self) -> List[List[Column]]:
        cols = super().unique_index_columns()
        cols.append([self.name_])
        return cols


class TableSites(TableEquipmentContainers):

    def name(self) -> str:
        return "sites"


class TableSubGeographicalRegions(TableIdentifiedObjects):
    geographical_region_mrid: Column = None

    def __init__(self):
        super().__init__()
        self.column_index += 1
        self.geographical_region_mrid = Column(self.column_index, "geographical_region_mrid", "TEXT", Nullable.NULL)

    def name(self) -> str:
        return "sub_geographical_regions"

    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super().non_unique_index_columns()
        cols.append([self.geographical_region_mrid])
        return cols


class TableSubstations(TableEquipmentContainers):
    sub_geographical_region_mrid: Column = None

    def __init__(self):
        super().__init__()
        self.column_index += 1
        self.sub_geographical_region_mrid = Column(self.column_index, "sub_geographical_region_mrid", "TEXT", Nullable.NULL)

    def name(self) -> str:
        return "substations"

    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super().non_unique_index_columns()
        cols.append([self.sub_geographical_region_mrid])
        return cols


class TableTerminals(TableAcDcTerminals):
    conducting_equipment_mrid: Column = None
    sequence_number: Column = None
    connectivity_node_mrid: Column = None
    phases: Column = None

    def __init__(self):
        super().__init__()
        self.column_index += 1
        self.conducting_equipment_mrid = Column(self.column_index, "conducting_equipment_mrid", "TEXT", Nullable.NULL)
        self.column_index += 1
        self.sequence_number = Column(self.column_index, "sequence_number", "INTEGER", Nullable.NOT_NULL)
        self.column_index += 1
        self.connectivity_node_mrid = Column(self.column_index, "connectivity_node_mrid", "TEXT", Nullable.NULL)
        self.column_index += 1
        self.phases = Column(self.column_index, "phases", "TEXT", Nullable.NOT_NULL)

    def name(self) -> str:
        return "terminals"

    def unique_index_columns(self) -> List[List[Column]]:
        cols = super().unique_index_columns()
        cols.append([self.conducting_equipment_mrid, self.sequence_number])
        return cols

    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super().non_unique_index_columns()
        cols.append([self.connectivity_node_mrid])
        return cols
