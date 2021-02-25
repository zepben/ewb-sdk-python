#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve import DiagramObject, TableDiagramObjects, Diagram, TableDiagrams, DiagramObjectPoint, TableDiagramObjectPoints
from zepben.evolve.database.sqlite.writers.base_cim_writer import BaseCIMWriter

__all__ = ["DiagramCIMWriter"]


class DiagramCIMWriter(BaseCIMWriter):

    # ************ IEC61970 DIAGRAM LAYOUT ************

    def save_diagram(self, diagram: Diagram) -> bool:
        table = self.database_tables.get_table(TableDiagrams)
        insert = self.database_tables.get_insert(TableDiagrams)

        insert.add_value(table.diagram_style.query_index, diagram.diagram_style.name)
        insert.add_value(table.orientation_kind.query_index, diagram.orientation_kind.name)

        return self.save_identified_object(table, insert, diagram, "diagram")

    def save_diagram_object(self, diagram_object: DiagramObject) -> bool:
        table = self.database_tables.get_table(TableDiagramObjects)
        insert = self.database_tables.get_insert(TableDiagramObjects)

        status = True
        for sequence, point in enumerate(diagram_object.points):
            status = status and self.save_diagram_object_point(diagram_object, point, sequence)
        insert.add_value(table.identified_object_mrid.query_index, diagram_object.identified_object_mrid)
        insert.add_value(table.diagram_mrid.query_index, self._mrid_or_none(diagram_object.diagram))
        insert.add_value(table.style.query_index, diagram_object.style)
        insert.add_value(table.rotation.query_index, diagram_object.rotation)

        return status and self.save_identified_object(table, insert, diagram_object, "diagram object")

    def save_diagram_object_point(self, diagram_object: DiagramObject, diagram_object_point: DiagramObjectPoint, sequence_number: int) -> bool:
        table = self.database_tables.get_table(TableDiagramObjectPoints)
        insert = self.database_tables.get_insert(TableDiagramObjectPoints)

        insert.add_value(table.diagram_object_mrid.query_index, diagram_object.mrid)
        insert.add_value(table.sequence_number.query_index, sequence_number)
        insert.add_value(table.x_position.query_index, diagram_object_point.x_position)
        insert.add_value(table.y_position.query_index, diagram_object_point.y_position)

        return self.try_execute_single_update(insert, "{}-point{}".format(diagram_object.mrid, sequence_number), "diagram object point")
