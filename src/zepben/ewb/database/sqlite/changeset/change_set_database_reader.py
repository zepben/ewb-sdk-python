#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["ChangeSetDatabaseReader"]

from sqlite3 import Connection

from zepben.ewb.database.sqlite.changeset.change_set_database_tables import ChangeSetDatabaseTables
from zepben.ewb.database.sqlite.changeset.change_set_service_reader import ChangeSetServiceReader
from zepben.ewb.database.sqlite.common.base_database_reader import BaseDatabaseReader
from zepben.ewb.database.sqlite.common.metadata_collection_reader import MetadataCollectionReader
from zepben.ewb.database.sqlite.tables.table_version import TableVersion
from zepben.ewb.services.variant.variant_service import VariantService


class ChangeSetDatabaseReader(BaseDatabaseReader):
    """
    A class for reading the `VariantService` objects and `MetadataCollection` from our change set database.

    :param connection: The connection to the database.
    :param service: The `VariantService` to populate with CIM objects from the database.
    :param database_description: The description of the database for logging (e.g. filename).
    """

    def __init__(
        self,
        connection: Connection,
        service: VariantService,
        database_description: str,
        tables: ChangeSetDatabaseTables = None,
        metadata_reader: MetadataCollectionReader = None,
        service_reader: ChangeSetServiceReader = None,
        table_version: TableVersion = None
    ):
        tables = tables if tables is not None else ChangeSetDatabaseTables()
        super().__init__(
            connection,
            metadata_reader if metadata_reader is not None else MetadataCollectionReader(service, tables, connection),
            service_reader if service_reader is not None else ChangeSetServiceReader(service, tables, connection),
            service,
            database_description,
            table_version if table_version is not None else TableVersion()
        )

    async def _post_load(self) -> bool:
        # The change set database is a partial view of the network, so the usual post load check for unresolved
        # references does not apply here.
        return True
