#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
__all__ = ["DiagramCimReader"]

from typing import Callable

from zepben.evolve.database.sqlite.common.base_cim_reader import BaseCimReader
from zepben.evolve.database.sqlite.extensions.result_set import ResultSet
from zepben.evolve.database.sqlite.tables.iec61970.base.diagramlayout.table_diagram_object_points import TableDiagramObjectPoints
from zepben.evolve.database.sqlite.tables.iec61970.base.diagramlayout.table_diagram_objects import TableDiagramObjects
from zepben.evolve.database.sqlite.tables.iec61970.base.diagramlayout.table_diagrams import TableDiagrams
from zepben.evolve.model.cim.iec61970.base.diagramlayout.diagram_layout import Diagram, DiagramObject, DiagramObjectPoint
from zepben.evolve.model.cim.iec61970.base.diagramlayout.diagram_style import DiagramStyle
from zepben.evolve.model.cim.iec61970.base.diagramlayout.orientation_kind import OrientationKind
from zepben.evolve.services.diagram.diagrams import DiagramService


class DiagramCimReader(BaseCimReader):
    """
    A class for reading the `DiagramService` tables from the database.

    :param service: The `DiagramService` to populate from the database.
    """

    def __init__(self, service: DiagramService):
        super().__init__(service)

    ###########################
    # IEC61970 Diagram Layout #
    ###########################

    def load_diagrams(self, table: TableDiagrams, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        """
        Create a `Diagram` and populate its fields from `TableDiagrams`.

        :param table: The database table to read the `Diagram` fields from.
        :param result_set: The record in the database table containing the fields for this `Diagram`.
        :param set_identifier: A callback to register the mRID of this `Diagram` for logging purposes.

        :return: True if the `Diagram` was successfully read from the database and added to the service.
        :raises SqlException: For any errors encountered reading from the database.
        """
        diagram = Diagram(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        diagram.diagram_style = DiagramStyle[result_set.get_string(table.diagram_style.query_index)]
        diagram.orientation_kind = OrientationKind[result_set.get_string(table.orientation_kind.query_index)]

        return self._load_identified_object(diagram, table, result_set) and self._add_or_throw(diagram)

    def load_diagram_objects(self, table: TableDiagramObjects, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        """
        Create a `DiagramObject` and populate its fields from `TableDiagramObjects`.

        :param table: The database table to read the `DiagramObject` fields from.
        :param result_set: The record in the database table containing the fields for this `DiagramObject`.
        :param set_identifier: A callback to register the mRID of this `DiagramObject` for logging purposes.

        :return: True if the `DiagramObject` was successfully read from the database and added to the service.
        :raises SqlException: For any errors encountered reading from the database.
        """
        diagram_object = DiagramObject(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        diagram_object.diagram = self._ensure_get(
            result_set.get_string(table.diagram_mrid.query_index, on_none=None),
            Diagram
        )
        if diagram_object.diagram is not None:
            diagram_object.diagram.add_diagram_object(diagram_object)

        diagram_object.identified_object_mrid = result_set.get_string(table.identified_object_mrid.query_index, on_none=None)
        diagram_object.style = result_set.get_string(table.style.query_index, on_none=None)
        diagram_object.rotation = result_set.get_float(table.rotation.query_index)

        return self._load_identified_object(diagram_object, table, result_set) and self._add_or_throw(diagram_object)

    def load_diagram_object_points(self, table: TableDiagramObjectPoints, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        """
        Create a `DiagramObjectPoint` and populate its fields from `TableDiagramObjectPoints`.

        :param table: The database table to read the `DiagramObjectPoint` fields from.
        :param result_set: The record in the database table containing the fields for this `DiagramObjectPoint`.
        :param set_identifier: A callback to register the mRID of this `DiagramObjectPoint` for logging purposes.

        :return: True if the `DiagramObjectPoint` was successfully read from the database and added to the service.
        :raises SqlException: For any errors encountered reading from the database.
        """
        diagram_object_mrid = set_identifier(result_set.get_string(table.diagram_object_mrid.query_index))
        sequence_number = result_set.get_int(table.sequence_number.query_index)

        set_identifier(f"{diagram_object_mrid}-point{sequence_number}")

        self._service.get(diagram_object_mrid, DiagramObject).insert_point(
            DiagramObjectPoint(
                result_set.get_float(table.x_position.query_index),
                result_set.get_float(table.y_position.query_index)
            ),
            sequence_number
        )

        return True
