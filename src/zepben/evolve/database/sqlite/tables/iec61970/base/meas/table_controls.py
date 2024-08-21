#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.meas.table_io_points import TableIoPoints

__all__ = ["TableControls"]


class TableControls(TableIoPoints):

    def __init__(self):
        super().__init__()
        self.power_system_resource_mrid: Column = self._create_column("power_system_resource_mrid", "TEXT", Nullable.NULL)

    @property
    def name(self) -> str:
        return "controls"
