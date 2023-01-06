#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.core_tables import TableIdentifiedObjects
from zepben.evolve.database.sqlite.tables.sqlite_table import SqliteTable

__all__ = ["TableDiagrams", "TableDiagramObjects", "TableDiagramObjects", "TableDiagramObjectPoints"]


class TableDiagramObjectPoints(SqliteTable):
    diagram_object_mrid: Column = None
    sequence_number: Column = None
    x_position: Column = None
    y_position: Column = None

    def __init__(self):
        super(TableDiagramObjectPoints, self).__init__()
        self.diagram_object_mrid = self._create_column("diagram_object_mrid", "TEXT", Nullable.NOT_NULL)
        self.sequence_number = self._create_column("sequence_number", "INTEGER", Nullable.NOT_NULL)
        self.x_position = self._create_column("x_position", "NUMBER", Nullable.NULL)
        self.y_position = self._create_column("y_position", "NUMBER", Nullable.NULL)

    def name(self) -> str:
        return "diagram_object_points"

    def unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableDiagramObjectPoints, self).unique_index_columns()
        cols.append([self.diagram_object_mrid, self.sequence_number])
        return cols

    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableDiagramObjectPoints, self).non_unique_index_columns()
        cols.append([self.diagram_object_mrid])
        return cols


class TableDiagramObjects(TableIdentifiedObjects):
    identified_object_mrid: Column = None
    diagram_mrid: Column = None
    style: Column = None
    rotation: Column = None

    def __init__(self):
        super(TableDiagramObjects, self).__init__()
        self.identified_object_mrid = self._create_column("identified_object_mrid", "TEXT", Nullable.NULL)
        self.diagram_mrid = self._create_column("diagram_mrid", "TEXT", Nullable.NULL)
        self.style = self._create_column("style", "TEXT", Nullable.NULL)
        self.rotation = self._create_column("rotation", "NUMBER", Nullable.NOT_NULL)

    def name(self) -> str:
        return "diagram_objects"

    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableDiagramObjects, self).non_unique_index_columns()
        cols.append([self.identified_object_mrid])
        cols.append([self.diagram_mrid])
        return cols


class TableDiagrams(TableIdentifiedObjects):
    diagram_style: Column = None
    orientation_kind: Column = None

    def __init__(self):
        super(TableDiagrams, self).__init__()
        self.diagram_style = self._create_column("diagram_style", "TEXT", Nullable.NOT_NULL)
        self.orientation_kind = self._create_column("orientation_kind", "TEXT", Nullable.NOT_NULL)

    def name(self) -> str:
        return "diagrams"
