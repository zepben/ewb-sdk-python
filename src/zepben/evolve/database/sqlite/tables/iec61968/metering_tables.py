#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61968.asset_tables import TableAssetContainers
from zepben.evolve.database.sqlite.tables.iec61970.base.core_tables import TableIdentifiedObjects

__all__ = ["TableEndDevices", "TableMeters", "TableUsagePoints"]


# noinspection PyAbstractClass
class TableEndDevices(TableAssetContainers):
    customer_mrid: Column = None
    service_location_mrid: Column = None

    def __init__(self):
        super(TableEndDevices, self).__init__()
        self.customer_mrid = self._create_column("customer_mrid", "TEXT", Nullable.NULL)
        self.service_location_mrid = self._create_column("service_location_mrid", "TEXT", Nullable.NULL)


class TableMeters(TableEndDevices):

    def name(self) -> str:
        return "meters"


class TableUsagePoints(TableIdentifiedObjects):
    location_mrid: Column = None
    is_virtual: Column = None
    connection_category: Column = None
    rated_power: Column = None
    approved_inverter_capacity: Column = None

    def __init__(self):
        super(TableUsagePoints, self).__init__()
        self.location_mrid = self._create_column("location_mrid", "TEXT", Nullable.NULL)
        self.is_virtual = self._create_column("is_virtual", "BOOLEAN")
        self.connection_category = self._create_column("connection_category", "TEXT", Nullable.NULL)
        self.rated_power = self._create_column("rated_power", "INTEGER", Nullable.NULL)
        self.approved_inverter_capacity = self._create_column("approved_inverter_capacity", "INTEGER", Nullable.NULL)

    def name(self) -> str:
        return "usage_points"
