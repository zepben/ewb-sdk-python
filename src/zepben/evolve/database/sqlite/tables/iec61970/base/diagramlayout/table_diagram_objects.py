#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List, Generator

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_identified_objects import TableIdentifiedObjects

__all__ = ["TableDiagramObjects"]


class TableDiagramObjects(TableIdentifiedObjects):

    def __init__(self):
        super().__init__()
        self.identified_object_mrid: Column = self._create_column("identified_object_mrid", "TEXT", Nullable.NULL)
        self.diagram_mrid: Column = self._create_column("diagram_mrid", "TEXT", Nullable.NULL)
        self.style: Column = self._create_column("style", "TEXT", Nullable.NULL)
        self.rotation: Column = self._create_column("rotation", "NUMBER", Nullable.NOT_NULL)

    @property
    def name(self) -> str:
        return "diagram_objects"

    @property
    def non_unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().non_unique_index_columns
        yield [self.identified_object_mrid]
        yield [self.diagram_mrid]
