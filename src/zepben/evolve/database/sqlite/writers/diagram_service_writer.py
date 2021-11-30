#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve import NetworkService, IdentifiedObject, DiagramObject, Diagram
from zepben.evolve.database.sqlite.writers.base_service_writer import BaseServiceWriter
from zepben.evolve.database.sqlite.writers.network_cim_writer import NetworkCIMWriter


class DiagramServiceWriter(BaseServiceWriter):

    def save(self, service: NetworkService, writer: NetworkCIMWriter) -> bool:
        status = super(DiagramServiceWriter, self).save(service, writer)

        for obj in service.objects(DiagramObject):
            status = status and self.validate_save(obj, writer.save_diagram_object)
        for obj in service.objects(Diagram):
            status = status and self.validate_save(obj, writer.save_diagram)

        return status




