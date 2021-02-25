#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve import DiagramObject, Diagram, DiagramService
from zepben.evolve.database.sqlite.writers.base_service_writer import BaseServiceWriter
from zepben.evolve.database.sqlite.writers.diagram_cim_writer import DiagramCIMWriter

__all__ = ["DiagramServiceWriter"]


class DiagramServiceWriter(BaseServiceWriter):

    def save(self, service: DiagramService, writer: DiagramCIMWriter) -> bool:
        status = super(DiagramServiceWriter, self).save(service, writer)

        for obj in service.objects(DiagramObject):
            status = status and self.validate_save(obj, writer.save_diagram_object)
        for obj in service.objects(Diagram):
            status = status and self.validate_save(obj, writer.save_diagram)

        return status
