#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["TableWireInfo"]

from abc import ABC

from zepben.ewb.database.sql.column import Column, Nullable
from zepben.ewb.database.sqlite.tables.iec61968.assets.table_asset_info import TableAssetInfo


class TableWireInfo(TableAssetInfo, ABC):

    def __init__(self):
        super().__init__()
        self.rated_current: Column = self._create_column("rated_current", "NUMBER", Nullable.NULL)
        self.material: Column = self._create_column("material", "TEXT", Nullable.NOT_NULL)
        self.size_description: Column = self._create_column("size_description", "TEXT", Nullable.NULL)
        self.strand_count: Column = self._create_column("strand_count", "TEXT", Nullable.NULL)
        self.core_strand_count: Column = self._create_column("core_strand_count", "TEXT", Nullable.NULL)
        self.insulated: Column = self._create_column("insulated", "BOOLEAN", Nullable.NULL)
        self.insulation_material: Column = self._create_column("insulation_material", "TEXT", Nullable.NOT_NULL)
        self.insulation_thickness: Column = self._create_column("insulation_thickness", "NUMBER", Nullable.NULL)
