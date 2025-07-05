#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from unittest.mock import create_autospec, call

from capture_mock_sequence import CaptureMockSequence
from zepben.evolve import DiagramService, DiagramCimWriter, DiagramServiceWriter, DiagramDatabaseTables
from zepben.evolve.model.cim.iec61970.base.diagramlayout.diagram import Diagram


class TestDiagramServiceWriter:

    #
    # NOTE: We don't do an exhaustive test of saving objects as this is done via the schema test.
    #

    def setup_method(self):
        self.diagram_service = DiagramService()
        self.cim_writer = create_autospec(DiagramCimWriter)
        self.diagram_service_writer = DiagramServiceWriter(self.diagram_service, create_autospec(DiagramDatabaseTables), self.cim_writer)

        self.cim_writer.save_diagram.return_value = True

        self.mock_sequence = CaptureMockSequence(
            cim_writer=self.cim_writer,
        )

    def test_passes_objects_through_to_the_cim_writer(self):
        diagram = Diagram()
        self.diagram_service.add(diagram)

        # NOTE: the save method will fail due to the relaxed mock returning false for all save operations,
        #       but a save should still be attempted on every object
        self.diagram_service_writer.save()

        self.mock_sequence.verify_sequence([call.cim_writer.save_diagram(diagram)])
