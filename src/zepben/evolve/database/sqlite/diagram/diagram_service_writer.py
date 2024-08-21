#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
__all__ = ["DiagramServiceWriter"]

from zepben.evolve.database.sqlite.common.base_service_writer import BaseServiceWriter
from zepben.evolve.database.sqlite.diagram.diagram_cim_writer import DiagramCimWriter
from zepben.evolve.database.sqlite.diagram.diagram_database_tables import DiagramDatabaseTables
from zepben.evolve.model.cim.iec61970.base.diagramlayout.diagram_layout import DiagramObject, Diagram
from zepben.evolve.services.diagram.diagrams import DiagramService


class DiagramServiceWriter(BaseServiceWriter):
    """
    A class for writing a `DiagramService` into the database.

    :param service: The `DiagramService` to save to the database.
    :param database_tables: The `DiagramDatabaseTables` to add to the database.
    """

    def __init__(
        self,
        service: DiagramService,
        database_tables: DiagramDatabaseTables,
        writer: DiagramCimWriter = None
    ):
        writer = writer if writer is not None else DiagramCimWriter(database_tables)
        super().__init__(service, writer)

        # This is not strictly necessary, it is just to update the type of the writer. It could be done with a generic
        # on the base class which looks like it works, but that actually silently breaks code insight and completion
        self._writer = writer

    def _do_save(self) -> bool:
        return all([
            self._save_each_object(DiagramObject, self._writer.save_diagram_object),
            self._save_each_object(Diagram, self._writer.save_diagram)
        ])
