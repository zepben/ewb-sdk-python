#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["TablePanDemandResponseFunctions"]

from zepben.ewb.database.sql.column import Column, Nullable
from zepben.ewb.database.sqlite.tables.iec61968.metering.table_end_device_functions import TableEndDeviceFunctions


class TablePanDemandResponseFunctions(TableEndDeviceFunctions):

    def __init__(self):
        super().__init__()
        self.kind: Column = self._create_column("kind", "TEXT", Nullable.NULL)
        self.appliance: Column = self._create_column("appliance", "INTEGER", Nullable.NULL)

    @property
    def name(self) -> str:
        return "pan_demand_response_functions"
