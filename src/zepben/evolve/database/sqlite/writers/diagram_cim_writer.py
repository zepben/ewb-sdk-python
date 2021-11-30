#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from dataclassy import dataclass

from zepben.evolve import DiagramObject, TableDiagramObjects, Diagram, TableDiagrams, DiagramObjectPoint, TableDiagramObjectPoints
from zepben.evolve.database.sqlite.writers.base_cim_writer import BaseCIMWriter


@dataclass
class DiagramCIMWriter(BaseCIMWriter):

    # ** ** ** ** ** ** IEC61970 DIAGRAM LAYOUT ** ** ** ** ** ** #

    def save_diagram(self, diagram: Diagram) -> bool:
        table = self.databaseTables.getTable(TableDiagrams)
        insert = self.databaseTables.getInsert(TableDiagrams)
        insert.add_value(table.DIAGRAM_STYLE.queryIndex, diagram.diagramStyle.name)
        insert.add_value(table.ORIENTATION_KIND.queryIndex, diagram.orientationKind.name)
        return self.save_identified_object(table, insert, diagram, "diagram")

    def save_diagram_object(self, diagram_object: DiagramObject) -> bool:
        table = self.databaseTables.getTable(TableDiagramObjects)
        insert = self.databaseTables.getInsert(TableDiagramObjects)
        status = True
        for sequence, point in enumerate(diagram_object.points):
            status = status and self.save_diagram_object_point(diagram_object, point, sequence) 
        insert.add_value(table.IDENTIFIED_OBJECT_MRID.queryIndex, diagram_object.identifiedObjectMRID)
        insert.add_value(table.DIAGRAM_MRID.queryIndex, diagram_object.diagram.mRID)
        insert.add_value(table.STYLE.queryIndex, diagram_object.style)
        insert.add_value(table.ROTATION.queryIndex, diagram_object.rotation)
        return status and self.save_identified_object(table, insert, diagram_object, "diagram object")

    def save_diagram_object_point(self, diagram_object: DiagramObject, diagram_object_point: DiagramObjectPoint, sequence_number: int) -> bool:
        table = self.databaseTables.getTable(TableDiagramObjectPoints)
        insert = self.databaseTables.getInsert(TableDiagramObjectPoints)
        insert.add_value(table.DIAGRAM_OBJECT_MRID.queryIndex, diagram_object.mRID)
        insert.add_value(table.SEQUENCE_NUMBER.queryIndex, sequence_number)
        insert.add_value(table.X_POSITION.queryIndex, diagram_object_point.xPosition)
        insert.add_value(table.Y_POSITION.queryIndex, diagram_object_point.yPosition)
        return self.try_execute_single_update(
            insert,
            "{}-point{}".format(diagram_object.mRID, sequence_number),
            "diagram object point"
        )

