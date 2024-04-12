#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Generator

from zepben.evolve.database.sqlite.common.base_database_tables import BaseDatabaseTables
from zepben.evolve.database.sqlite.tables.iec61970.base.diagramlayout.table_diagram_object_points import *
from zepben.evolve.database.sqlite.tables.iec61970.base.diagramlayout.table_diagram_objects import *
from zepben.evolve.database.sqlite.tables.iec61970.base.diagramlayout.table_diagrams import *
from zepben.evolve.database.sqlite.tables.sqlite_table import *

__all__ = ["DiagramDatabaseTables"]


class DiagramDatabaseTables(BaseDatabaseTables):
    """
    The collection of tables for our customer databases.
    """

    @property
    def _included_tables(self) -> Generator[SqliteTable, None, None]:
        for table in super()._included_tables:
            yield table

        yield TableDiagramObjectPoints()
        yield TableDiagramObjects()
        yield TableDiagrams()
