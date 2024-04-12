#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
__all__ = ["DiagramServiceReader"]

from sqlite3 import Connection

from zepben.evolve.database.sqlite.common.base_service_reader import BaseServiceReader
from zepben.evolve.database.sqlite.diagram.diagram_cim_reader import DiagramCimReader
from zepben.evolve.database.sqlite.diagram.diagram_database_tables import DiagramDatabaseTables
from zepben.evolve.database.sqlite.tables.iec61970.base.diagramlayout.table_diagram_object_points import TableDiagramObjectPoints
from zepben.evolve.database.sqlite.tables.iec61970.base.diagramlayout.table_diagram_objects import TableDiagramObjects
from zepben.evolve.database.sqlite.tables.iec61970.base.diagramlayout.table_diagrams import TableDiagrams
from zepben.evolve.services.diagram.diagrams import DiagramService


class DiagramServiceReader(BaseServiceReader):
    """
    A class for reading a `DiagramService` from the database.

    :param service: The `DiagramService` to populate from the database.
    :param database_tables: The tables available in the database.
    :param connection: A connection to the database.

    :param reader: The `DiagramCimReader` used to load the objects from the database.
    """

    def __init__(
        self,
        service: DiagramService,
        database_tables: DiagramDatabaseTables,
        connection: Connection,
        reader: DiagramCimReader = None
    ):
        reader = reader if reader is not None else DiagramCimReader(service)
        super().__init__(database_tables, connection, reader)

        # This is not strictly necessary, it is just to update the type of the reader. It could be done with a generic
        # on the base class which looks like it works, but that actually silently breaks code insight and completion
        self._reader = reader

    def _do_load(self) -> bool:
        return all([
            self._load_each(TableDiagrams, self._reader.load_diagrams),
            self._load_each(TableDiagramObjects, self._reader.load_diagram_objects),
            self._load_each(TableDiagramObjectPoints, self._reader.load_diagram_object_points)
        ])
