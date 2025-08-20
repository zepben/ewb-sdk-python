#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["TableCurrentTransformers"]

from zepben.ewb.database.sql.column import Column, Nullable
from zepben.ewb.database.sqlite.tables.iec61970.base.auxiliaryequipment.table_sensors import TableSensors


class TableCurrentTransformers(TableSensors):

    def __init__(self):
        super().__init__()
        self.current_transformer_info_mrid: Column = self._create_column("current_transformer_info_mrid", "TEXT", Nullable.NULL)
        self.core_burden: Column = self._create_column("core_burden", "INTEGER", Nullable.NULL)

    @property
    def name(self) -> str:
        return "current_transformers"
