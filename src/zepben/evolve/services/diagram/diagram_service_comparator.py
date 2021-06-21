#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.evolve import BaseServiceComparator, ObjectDifference, Diagram, DiagramObject


#
# NOTE: The functions below are accessed by reflection rather than directly. Make sure you check the code coverage
#       to ensure they are covered correctly.
#
class DiagramServiceComparator(BaseServiceComparator):
    """
    Compare the objects supported by the diagram service.
    """

    def _compare_diagram(self, source: Diagram, target: Diagram) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_values(diff, Diagram.diagram_style, Diagram.orientation_kind)
        self._compare_id_reference_collections(diff, Diagram.diagram_objects)

        return self._compare_identified_object(diff)

    def _compare_diagram_object(self, source: DiagramObject, target: DiagramObject) -> ObjectDifference:
        diff = ObjectDifference(source, target)

        self._compare_id_references(diff, DiagramObject.diagram)
        self._compare_values(diff, DiagramObject.identified_object_mrid, DiagramObject.style)
        self._compare_floats(diff, DiagramObject.rotation)
        self._compare_indexed_value_collections(diff, DiagramObject.points)

        return self._compare_identified_object(diff)
