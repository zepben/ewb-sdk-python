#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from test.database.sqlite.tables.table_test_utils import verify_column
from zepben.evolve import Nullable, TableDiagramObjectPoints, TableDiagramObjects, TableDiagrams


def test_table_diagram_object_points():
    t = TableDiagramObjectPoints()
    verify_column(t.diagram_object_mrid, 1, "diagram_object_mrid", "TEXT", Nullable.NOT_NULL)
    verify_column(t.sequence_number, 2, "sequence_number", "INTEGER", Nullable.NOT_NULL)
    verify_column(t.x_position, 3, "x_position", "NUMBER", Nullable.NULL)
    verify_column(t.y_position, 4, "y_position", "NUMBER", Nullable.NULL)
    assert t.unique_index_columns() == [[t.diagram_object_mrid, t.sequence_number]]
    assert t.non_unique_index_columns() == [[t.diagram_object_mrid]]
    assert t.name() == "diagram_object_points"


def test_table_diagram_objects():
    t = TableDiagramObjects()
    verify_column(t.identified_object_mrid, 5, "identified_object_mrid", "TEXT", Nullable.NULL)
    verify_column(t.diagram_mrid, 6, "diagram_mrid", "TEXT", Nullable.NULL)
    verify_column(t.style, 7, "style", "TEXT", Nullable.NOT_NULL)
    verify_column(t.rotation, 8, "rotation", "NUMBER", Nullable.NOT_NULL)
    assert t.name() == "diagram_objects"
    assert t.non_unique_index_columns() == [[t.name_], [t.identified_object_mrid], [t.diagram_mrid]]


def test_table_diagrams():
    t = TableDiagrams()
    verify_column(t.diagram_style, 5, "diagram_style", "TEXT", Nullable.NOT_NULL)
    verify_column(t.orientation_kind, 6, "orientation_kind", "TEXT", Nullable.NOT_NULL)
    assert t.name() == "diagrams"
