#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61968.assets.table_structures import TableStructures

__all__ = ["TablePoles"]


class TablePoles(TableStructures):

    def __init__(self):
        super().__init__()
        self.classification: Column = self._create_column("classification", "TEXT", Nullable.NOT_NULL)

    @property
    def name(self) -> str:
        return "poles"
