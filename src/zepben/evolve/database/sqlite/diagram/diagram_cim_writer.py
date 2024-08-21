#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
__all__ = ["DiagramCimWriter"]

from zepben.evolve.database.sqlite.common.base_cim_writer import BaseCimWriter
from zepben.evolve.database.sqlite.diagram.diagram_database_tables import DiagramDatabaseTables
from zepben.evolve.database.sqlite.tables.iec61970.base.diagramlayout.table_diagram_object_points import TableDiagramObjectPoints
from zepben.evolve.database.sqlite.tables.iec61970.base.diagramlayout.table_diagram_objects import TableDiagramObjects
from zepben.evolve.database.sqlite.tables.iec61970.base.diagramlayout.table_diagrams import TableDiagrams
from zepben.evolve.model.cim.iec61970.base.diagramlayout.diagram_layout import Diagram, DiagramObject, DiagramObjectPoint


class DiagramCimWriter(BaseCimWriter):
    """
    A class for writing the `DiagramService` tables to the database.

    :param database_tables: The tables available in the database.
    """

    def __init__(self, database_tables: DiagramDatabaseTables):
        super().__init__(database_tables)

    ###########################
    # IEC61970 Diagram Layout #
    ###########################

    def save_diagram(self, diagram: Diagram) -> bool:
        """
        Save the `Diagram` fields to `TableDiagrams`.

        :param diagram: The `Diagram` instance to write to the database.

        :return: True if the `Diagram` was successfully written to the database, otherwise false.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableDiagrams)
        insert = self._database_tables.get_insert(TableDiagrams)

        insert.add_value(table.diagram_style.query_index, diagram.diagram_style.name)
        insert.add_value(table.orientation_kind.query_index, diagram.orientation_kind.name)

        return self._save_identified_object(table, insert, diagram, "diagram")

    def save_diagram_object(self, diagram_object: DiagramObject) -> bool:
        """
        Save the `DiagramObject` fields to `TableDiagramObjects`.

        :param diagram_object: The `DiagramObject` instance to write to the database.

        :return: True if the `DiagramObject` was successfully written to the database, otherwise false.
        :raises SqlException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableDiagramObjects)
        insert = self._database_tables.get_insert(TableDiagramObjects)

        status = True
        for sequence, point in enumerate(diagram_object.points):
            status = all([status, self._save_diagram_object_point(diagram_object, point, sequence)])

        insert.add_value(table.identified_object_mrid.query_index, diagram_object.identified_object_mrid)
        insert.add_value(table.diagram_mrid.query_index, self._mrid_or_none(diagram_object.diagram))
        insert.add_value(table.style.query_index, diagram_object.style)
        insert.add_value(table.rotation.query_index, diagram_object.rotation)

        return all([status, self._save_identified_object(table, insert, diagram_object, "diagram object")])

    def _save_diagram_object_point(self, diagram_object: DiagramObject, diagram_object_point: DiagramObjectPoint, sequence_number: int) -> bool:
        table = self._database_tables.get_table(TableDiagramObjectPoints)
        insert = self._database_tables.get_insert(TableDiagramObjectPoints)

        insert.add_value(table.diagram_object_mrid.query_index, diagram_object.mrid)
        insert.add_value(table.sequence_number.query_index, sequence_number)
        insert.add_value(table.x_position.query_index, diagram_object_point.x_position)
        insert.add_value(table.y_position.query_index, diagram_object_point.y_position)

        return self._try_execute_single_update(insert, "diagram object point")
