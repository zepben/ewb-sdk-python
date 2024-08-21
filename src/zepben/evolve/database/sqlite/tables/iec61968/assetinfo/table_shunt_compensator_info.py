#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61968.assets.table_asset_info import TableAssetInfo

__all__ = ["TableShuntCompensatorInfo"]


class TableShuntCompensatorInfo(TableAssetInfo):

    def __init__(self):
        super().__init__()
        self.max_power_loss: Column = self._create_column("max_power_loss", "INTEGER", Nullable.NULL)
        self.rated_current: Column = self._create_column("rated_current", "INTEGER", Nullable.NULL)
        self.rated_reactive_power: Column = self._create_column("rated_reactive_power", "INTEGER", Nullable.NULL)
        self.rated_voltage: Column = self._create_column("rated_voltage", "INTEGER", Nullable.NULL)

    @property
    def name(self) -> str:
        return "shunt_compensator_info"
