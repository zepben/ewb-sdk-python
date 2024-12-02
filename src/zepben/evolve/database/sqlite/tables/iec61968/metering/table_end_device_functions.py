#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from abc import ABC

from zepben.evolve.database.sqlite.tables.column import Column, Nullable

__all__ = ["TableEndDeviceFunctions"]

from zepben.evolve.database.sqlite.tables.iec61968.assets.table_asset_functions import TableAssetFunctions


class TableEndDeviceFunctions(TableAssetFunctions, ABC):

    def __init__(self):
        super().__init__()
        self.end_device_mrid: Column = self._create_column("end_device_mrid", "TEXT", Nullable.NULL)
        self.enabled: Column = self._create_column("enabled", "BOOLEAN", Nullable.NOT_NULL)
