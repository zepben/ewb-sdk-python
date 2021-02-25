#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.core_tables import TableIdentifiedObjects

__all__ = ["TableRemotePoints", "TableRemoteControls", "TableRemoteSources"]


# noinspection PyAbstractClass
class TableRemotePoints(TableIdentifiedObjects):
    pass


class TableRemoteControls(TableRemotePoints):
    control_mrid: Column = None

    def __init__(self):
        super(TableRemoteControls, self).__init__()
        self.control_mrid = self._create_column("control_mrid", "TEXT", Nullable.NULL)

    def name(self) -> str:
        return "remote_controls"


class TableRemoteSources(TableRemotePoints):
    measurement_mrid: Column = None

    def __init__(self):
        super(TableRemoteSources, self).__init__()
        self.measurement_mrid = self._create_column("measurement_mrid", "TEXT", Nullable.NULL)

    def name(self) -> str:
        return "remote_sources"
