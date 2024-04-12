#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61968.assets.table_assets import TableAssets

__all__ = ["TableStreetlights"]


class TableStreetlights(TableAssets):

    def __init__(self):
        super().__init__()
        self.pole_mrid: Column = self._create_column("pole_mrid", "TEXT", Nullable.NULL)
        self.lamp_kind: Column = self._create_column("lamp_kind", "TEXT", Nullable.NOT_NULL)
        self.light_rating: Column = self._create_column("light_rating", "INTEGER", Nullable.NULL)

    @property
    def name(self) -> str:
        return "streetlights"
