#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import List

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.sqlite_table import SqliteTable

__all__ = ["TableEquipmentEquipmentContainers", "TableEquipmentUsagePoints", "TableEquipmentOperationalRestrictions"]


class TableEquipmentEquipmentContainers(SqliteTable):
    equipment_mrid: Column = None
    equipment_container_mrid: Column = None

    def __init__(self):
        super(TableEquipmentEquipmentContainers, self).__init__()
        self.column_index += 1
        self.equipment_mrid = Column(self.column_index, "equipment_mrid", "TEXT", Nullable.NOT_NULL)
        self.column_index += 1
        self.equipment_container_mrid = Column(self.column_index, "equipment_container_mrid", "TEXT", Nullable.NOT_NULL)

    def name(self) -> str:
        return "equipment_equipment_containers"

    def unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableEquipmentEquipmentContainers, self).unique_index_columns()
        cols.append([self.equipment_mrid, self.equipment_container_mrid])
        return cols

    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableEquipmentEquipmentContainers, self).non_unique_index_columns()
        cols.append([self.equipment_mrid])
        cols.append([self.equipment_container_mrid])
        return cols


class TableEquipmentOperationalRestrictions(SqliteTable):
    equipment_mrid: Column = None
    operational_restriction_mrid: Column = None

    def __init__(self):
        super(TableEquipmentOperationalRestrictions, self).__init__()
        self.column_index += 1
        self.equipment_mrid = Column(self.column_index, "equipment_mrid", "TEXT", Nullable.NOT_NULL)
        self.column_index += 1
        self.operational_restriction_mrid = Column(self.column_index, "operational_restriction_mrid", "TEXT", Nullable.NOT_NULL)

    def name(self) -> str:
        return "equipment_operational_restrictions"

    def unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableEquipmentOperationalRestrictions, self).unique_index_columns()
        cols.append([self.equipment_mrid, self.operational_restriction_mrid])
        return cols

    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableEquipmentOperationalRestrictions, self).non_unique_index_columns()
        cols.append([self.equipment_mrid])
        cols.append([self.operational_restriction_mrid])
        return cols


class TableEquipmentUsagePoints(SqliteTable):
    equipment_mrid: Column = None
    usage_point_mrid: Column = None

    def __init__(self):
        super(TableEquipmentUsagePoints, self).__init__()
        self.column_index += 1
        self.equipment_mrid = Column(self.column_index, "equipment_mrid", "TEXT", Nullable.NOT_NULL)
        self.column_index += 1
        self.usage_point_mrid = Column(self.column_index, "usage_point_mrid", "TEXT", Nullable.NOT_NULL)

    def name(self) -> str:
        return "equipment_usage_points"

    def unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableEquipmentUsagePoints, self).unique_index_columns()
        cols.append([self.equipment_mrid, self.usage_point_mrid])
        return cols

    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableEquipmentUsagePoints, self).non_unique_index_columns()
        cols.append([self.equipment_mrid])
        cols.append([self.usage_point_mrid])
        return cols
