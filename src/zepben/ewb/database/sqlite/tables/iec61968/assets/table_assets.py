#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["TableAssets"]

from abc import ABC

from zepben.ewb.database.sqlite.tables.column import Column, Nullable
from zepben.ewb.database.sqlite.tables.iec61970.base.core.table_identified_objects import TableIdentifiedObjects


class TableAssets(TableIdentifiedObjects, ABC):

    def __init__(self):
        super().__init__()
        self.location_mrid: Column = self._create_column("location_mrid", "TEXT", Nullable.NULL)
