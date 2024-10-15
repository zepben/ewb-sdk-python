#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_identified_objects import TableIdentifiedObjects


class TableUsagePoints(TableIdentifiedObjects):

    def __init__(self):
        super().__init__()
        self.location_mrid: Column = self._create_column("location_mrid", "TEXT", Nullable.NULL)
        self.is_virtual: Column = self._create_column("is_virtual", "BOOLEAN")
        self.connection_category: Column = self._create_column("connection_category", "TEXT", Nullable.NULL)
        self.rated_power: Column = self._create_column("rated_power", "INTEGER", Nullable.NULL)
        self.approved_inverter_capacity: Column = self._create_column("approved_inverter_capacity", "INTEGER", Nullable.NULL)
        self.phase_code: Column = self._create_column("phase_code", "TEXT", Nullable.NOT_NULL)

    @property
    def name(self) -> str:
        return "usage_points"
