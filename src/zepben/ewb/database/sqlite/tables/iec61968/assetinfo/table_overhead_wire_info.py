#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["TableOverheadWireInfo"]

from zepben.ewb.database.sqlite.tables.iec61968.assetinfo.table_wire_info import TableWireInfo


class TableOverheadWireInfo(TableWireInfo):

    @property
    def name(self) -> str:
        return "overhead_wire_info"
