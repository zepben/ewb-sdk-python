#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["TablePoles"]

from zepben.ewb.database.sql.column import Column, Nullable
from zepben.ewb.database.sqlite.tables.iec61968.assets.table_structures import TableStructures


class TablePoles(TableStructures):

    def __init__(self):
        super().__init__()
        self.classification: Column = self._create_column("classification", "TEXT", Nullable.NULL)

    @property
    def name(self) -> str:
        return "poles"
