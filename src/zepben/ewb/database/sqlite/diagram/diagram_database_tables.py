#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["DiagramDatabaseTables"]

from typing import Generator

from zepben.ewb.database.sqlite.common.base_database_tables import BaseDatabaseTables
from zepben.ewb.database.sqlite.tables.iec61970.base.diagramlayout.table_diagram_object_points import *
from zepben.ewb.database.sqlite.tables.iec61970.base.diagramlayout.table_diagram_objects import *
from zepben.ewb.database.sqlite.tables.iec61970.base.diagramlayout.table_diagrams import *
from zepben.ewb.database.sqlite.tables.sqlite_table import *


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
