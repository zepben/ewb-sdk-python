#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["TableGroundDisconnectors"]

from zepben.ewb.database.sqlite.tables.iec61970.base.wires.table_switches import TableSwitches


class TableGroundDisconnectors(TableSwitches):

    @property
    def name(self) -> str:
        return "ground_disconnectors"
