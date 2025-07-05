#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from services.common.service_comparator_validator import ServiceComparatorValidator
from services.common.test_base_service_comparator import TestBaseServiceComparator
from zepben.evolve import DiagramService, DiagramStyle, OrientationKind
from zepben.evolve.model.cim.iec61970.base.diagramlayout.diagram import Diagram
from zepben.evolve.model.cim.iec61970.base.diagramlayout.diagram_object import DiagramObject
from zepben.evolve.model.cim.iec61970.base.diagramlayout.diagram_object_point import DiagramObjectPoint
from zepben.evolve.services.diagram.diagram_service_comparator import DiagramServiceComparator


class TestDiagramServiceComparator(TestBaseServiceComparator):
    validator = ServiceComparatorValidator(lambda: DiagramService(), lambda _: DiagramServiceComparator())

    def test_compare_diagram_attributes(self):
        self._compare_identified_object(Diagram)

        self.validator.validate_property(Diagram.diagram_style, Diagram, lambda _: DiagramStyle.SCHEMATIC, lambda _: DiagramStyle.GEOGRAPHIC)
        self.validator.validate_property(Diagram.orientation_kind, Diagram, lambda _: OrientationKind.POSITIVE, lambda _: OrientationKind.NEGATIVE)
        self.validator.validate_collection(
            Diagram.diagram_objects, Diagram.add_diagram_object,
            Diagram,
            lambda it: DiagramObject(mrid="1", diagram=it),
            lambda it: DiagramObject(mrid="2", diagram=it))

    def test_compare_diagram_object_attributes(self):
        self._compare_identified_object(DiagramObject)

        self.validator.validate_property(DiagramObject.diagram, DiagramObject, lambda _: Diagram(mrid="d1"), lambda _: Diagram(mrid="d2"))
        self.validator.validate_property(DiagramObject.identified_object_mrid, DiagramObject, lambda _: "dio1", lambda _: "dio2")
        self.validator.validate_property(DiagramObject.style, DiagramObject, lambda _: "JUNCTION", lambda _: "CB")
        self.validator.validate_property(DiagramObject.rotation, DiagramObject, lambda _: 0.0, lambda _: 1.1)
        self.validator.validate_indexed_collection(
            DiagramObject.points,
            DiagramObject.add_point,
            DiagramObject,
            lambda _: DiagramObjectPoint(1.0, 2.0),
            lambda _: DiagramObjectPoint(3.0, 4.0)
        )
