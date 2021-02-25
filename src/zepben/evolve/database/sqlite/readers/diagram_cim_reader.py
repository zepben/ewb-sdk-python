#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Callable

from zepben.evolve import BaseCIMReader, TableDiagrams, ResultSet, Diagram, DiagramStyle, OrientationKind, TableDiagramObjects, DiagramObject, \
    TableDiagramObjectPoints, DiagramObjectPoint, DiagramService

__all__ = ["DiagramCIMReader"]

from zepben.evolve.database.sqlite.readers.base_cim_reader import DuplicateMRIDException


class DiagramCIMReader(BaseCIMReader):
    _diagram_service: DiagramService

    def __init__(self, diagram_service: DiagramService):
        super().__init__(diagram_service)

    # ************ IEC61970 DIAGRAM LAYOUT ************

    def load_diagram(self, table: TableDiagrams, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        diagram = Diagram(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        diagram.diagram_style = DiagramStyle[rs.get_string(table.diagram_style.query_index)]
        diagram.orientation_kind = OrientationKind[rs.get_string(table.orientation_kind.query_index)]

        return self._load_identified_object(diagram, table, rs) and self._add_or_throw(diagram)

    def load_diagram_object(self, table: TableDiagramObjects, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        diagram_object = DiagramObject(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        diagram = self._ensure_get(rs.get_string(table.diagram_mrid.query_index, None), Diagram)
        if diagram is not None:
            diagram.add_diagram_object(diagram_object)

        diagram_object.identified_object_mrid = rs.get_string(table.identified_object_mrid.query_index, None)
        diagram_object.style = rs.get_string(table.style.query_index, None)
        diagram_object.rotation = rs.get_double(table.rotation.query_index)

        if not self._load_identified_object(diagram_object, table, rs):
            return False

        # noinspection PyUnresolvedReferences
        if self._base_service.add_diagram_object(diagram_object):
            return True
        else:
            raise DuplicateMRIDException(
                f"Failed to load {diagram_object}. Unable to add to service '{self._base_service.name}': duplicate MRID ({self._base_service.get(diagram_object.mrid)})"
            )

    def load_diagram_object_point(self, table: TableDiagramObjectPoints, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        diagram_object_mrid = set_last_mrid(rs.get_string(table.diagram_object_mrid.query_index))
        sequence_number = rs.get_int(table.sequence_number.query_index)

        set_last_mrid(f"{diagram_object_mrid}-point{sequence_number}")

        # noinspection PyArgumentList
        diagram_object_point = DiagramObjectPoint(
            rs.get_double(table.x_position.query_index),
            rs.get_double(table.y_position.query_index)
        )

        diagram_object = self._base_service.get(diagram_object_mrid, DiagramObject)
        diagram_object.insert_point(diagram_object_point, sequence_number)

        return True
