#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["TableRelayInfo"]

from zepben.ewb.database.sql.column import Column, Nullable
from zepben.ewb.database.sqlite.tables.iec61968.assets.table_asset_info import TableAssetInfo


class TableRelayInfo(TableAssetInfo):

    def __init__(self):
        super().__init__()
        self.curve_setting: Column = self._create_column("curve_setting", "TEXT", Nullable.NULL)
        self.reclose_fast: Column = self._create_column("reclose_fast", "BOOLEAN", Nullable.NULL)

    @property
    def name(self) -> str:
        return "relay_info"
