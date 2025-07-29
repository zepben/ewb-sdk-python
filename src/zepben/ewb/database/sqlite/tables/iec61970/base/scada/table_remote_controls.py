#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["TableRemoteControls"]

from zepben.ewb.database.sql.column import Column, Nullable
from zepben.ewb.database.sqlite.tables.iec61970.base.scada.table_remote_points import TableRemotePoints


class TableRemoteControls(TableRemotePoints):

    def __init__(self):
        super().__init__()
        self.control_mrid: Column = self._create_column("control_mrid", "TEXT", Nullable.NULL)

    @property
    def name(self) -> str:
        return "remote_controls"
