#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.evolve import BaseServiceReader, TableDiagrams, TableDiagramObjects, TableDiagramObjectPoints, DiagramCIMReader

__all__ = ["DiagramServiceReader"]


class DiagramServiceReader(BaseServiceReader):
    """
    Class for reading a `DiagramService` from the database.
    """

    def load(self, reader: DiagramCIMReader) -> bool:
        status = self.load_name_types(reader)

        status = status and self._load_each(TableDiagrams, "diagrams", reader.load_diagram)
        status = status and self._load_each(TableDiagramObjects, "diagram objects", reader.load_diagram_object)
        status = status and self._load_each(TableDiagramObjectPoints, "diagram object points", reader.load_diagram_object_point)

        status = status and self.load_names(reader)

        return status
