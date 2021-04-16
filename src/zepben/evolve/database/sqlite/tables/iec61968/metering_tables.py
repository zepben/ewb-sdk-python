#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61968.asset_tables import TableAssetContainers
from zepben.evolve.database.sqlite.tables.iec61970.base.core_tables import TableIdentifiedObjects

__all__ = ["TableEndDevices", "TableMeters", "TableUsagePoints"]


class TableEndDevices(TableAssetContainers):
    customer_mrid: Column = None
    service_location_mrid: Column = None

    def __init__(self):
        super(TableEndDevices, self).__init__()
        self.column_index += 1
        self.customer_mrid = Column(self.column_index, "customer_mrid", "TEXT", Nullable.NULL)
        self.column_index += 1
        self.service_location_mrid = Column(self.column_index, "service_location_mrid", "TEXT", Nullable.NULL)


class TableMeters(TableEndDevices):

    def name(self) -> str:
        return "meters"


class TableUsagePoints(TableIdentifiedObjects):
    location_mrid: Column = None

    def __init__(self):
        super(TableUsagePoints, self).__init__()
        self.column_index += 1
        self.location_mrid = Column(self.column_index, "location_mrid", "TEXT", Nullable.NULL)

    def name(self) -> str:
        return "usage_points"
