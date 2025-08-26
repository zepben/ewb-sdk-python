#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["TableAnalogs"]

from zepben.ewb.database.sql.column import Column, Nullable
from zepben.ewb.database.sqlite.tables.iec61970.base.meas.table_measurements import TableMeasurements


class TableAnalogs(TableMeasurements):

    def __init__(self):
        super().__init__()
        self.positive_flow_in: Column = self._create_column("positive_flow_in", "BOOLEAN", Nullable.NULL)

    @property
    def name(self) -> str:
        return "analogs"
