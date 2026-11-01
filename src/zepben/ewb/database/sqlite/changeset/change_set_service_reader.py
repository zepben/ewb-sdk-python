#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["ChangeSetServiceReader"]

from sqlite3 import Connection

from zepben.ewb.database.sqlite.changeset.change_set_cim_reader import ChangeSetCimReader
from zepben.ewb.database.sqlite.changeset.change_set_database_tables import ChangeSetDatabaseTables
from zepben.ewb.database.sqlite.common.base_service_reader import BaseServiceReader
from zepben.ewb.database.sqlite.tables.iec61970.infiec61970.part303.genericdataset.table_change_sets import TableChangeSets
from zepben.ewb.database.sqlite.tables.iec61970.infiec61970.part303.genericdataset.table_object_creations import \
    TableObjectCreations
from zepben.ewb.database.sqlite.tables.iec61970.infiec61970.part303.genericdataset.table_object_deletions import \
    TableObjectDeletions
from zepben.ewb.database.sqlite.tables.iec61970.infiec61970.part303.genericdataset.table_object_modifications import \
    TableObjectModifications
from zepben.ewb.services.variant.variant_service import VariantService


class ChangeSetServiceReader(BaseServiceReader):
    """
    A class for reading a `VariantService` from the database.

    :param service: The `VariantService` to populate from the database.
    :param database_tables: The tables available in the database.
    :param connection: A connection to the database.
    """

    def __init__(
        self,
        service: VariantService,
        database_tables: ChangeSetDatabaseTables,
        connection: Connection,
        reader: ChangeSetCimReader = None
    ):
        reader = reader if reader is not None else ChangeSetCimReader(service)
        super().__init__(database_tables, connection, reader)

        # This is not strictly necessary, it is just to update the type of the reader. It could be done with a generic
        # on the base class which looks like it works, but that actually silently breaks code insight and completion
        self._reader: ChangeSetCimReader = reader

    def _do_load(self) -> bool:
        return all([
            self._load_each(TableChangeSets, self._reader.load_change_sets),
            self._load_each(TableObjectCreations, self._reader.load_object_creations),
            self._load_each(TableObjectDeletions, self._reader.load_object_deletions),
            self._load_each(TableObjectModifications, self._reader.load_object_modifications)
        ])
