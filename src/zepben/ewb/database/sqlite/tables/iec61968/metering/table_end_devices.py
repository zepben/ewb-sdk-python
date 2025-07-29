#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["TableEndDevices"]

from abc import ABC

from zepben.ewb.database.sql.column import Column, Nullable
from zepben.ewb.database.sqlite.tables.iec61968.assets.table_asset_containers import TableAssetContainers


class TableEndDevices(TableAssetContainers, ABC):

    def __init__(self):
        super().__init__()
        self.customer_mrid: Column = self._create_column("customer_mrid", "TEXT", Nullable.NULL)
        self.service_location_mrid: Column = self._create_column("service_location_mrid", "TEXT", Nullable.NULL)
