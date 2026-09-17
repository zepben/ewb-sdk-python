#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["ChangeSetDatabaseTables"]

from typing import Generator

from zepben.ewb.database.sqlite.common.base_database_tables import BaseDatabaseTables
from zepben.ewb.database.sqlite.tables.iec61970.infiec61970.part303.genericdataset.table_change_sets import \
    TableChangeSets
from zepben.ewb.database.sqlite.tables.iec61970.infiec61970.part303.genericdataset.table_object_creations import \
    TableObjectCreations
from zepben.ewb.database.sqlite.tables.iec61970.infiec61970.part303.genericdataset.table_object_deletions import \
    TableObjectDeletions
from zepben.ewb.database.sqlite.tables.iec61970.infiec61970.part303.genericdataset.table_object_modifications import \
    TableObjectModifications
from zepben.ewb.database.sqlite.tables.sqlite_table import SqliteTable


class ChangeSetDatabaseTables(BaseDatabaseTables):
    """
    The collection of tables for our change set databases.
    """

    @property
    def _included_tables(self) -> Generator[SqliteTable, None, None]:
        yield from super()._included_tables

        yield TableChangeSets()
        yield TableObjectCreations()
        yield TableObjectDeletions()
        yield TableObjectModifications()
