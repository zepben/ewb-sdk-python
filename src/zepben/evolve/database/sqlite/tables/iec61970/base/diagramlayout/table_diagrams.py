#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_identified_objects import TableIdentifiedObjects

__all__ = ["TableDiagrams"]


class TableDiagrams(TableIdentifiedObjects):

    def __init__(self):
        super().__init__()
        self.diagram_style: Column = self._create_column("diagram_style", "TEXT", Nullable.NOT_NULL)
        self.orientation_kind: Column = self._create_column("orientation_kind", "TEXT", Nullable.NOT_NULL)

    @property
    def name(self) -> str:
        return "diagrams"
