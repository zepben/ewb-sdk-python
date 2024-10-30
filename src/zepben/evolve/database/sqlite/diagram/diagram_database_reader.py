#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
__all__ = ["DiagramDatabaseReader"]

from sqlite3 import Connection

from zepben.evolve.database.sqlite.common.base_database_reader import BaseDatabaseReader
from zepben.evolve.database.sqlite.common.metadata_collection_reader import MetadataCollectionReader
from zepben.evolve.database.sqlite.diagram.diagram_database_tables import DiagramDatabaseTables
from zepben.evolve.database.sqlite.diagram.diagram_service_reader import DiagramServiceReader
from zepben.evolve.database.sqlite.tables.table_version import TableVersion
from zepben.evolve.services.diagram.diagrams import DiagramService


class DiagramDatabaseReader(BaseDatabaseReader):
    """
    A class for reading the `DiagramService` objects and `MetadataCollection` from our diagram database.

    :param connection: The connection to the database.
    :param service: The `DiagramService` to populate with CIM objects from the database.
    :param database_description: The description of the database for logging (e.g. filename).
    """

    def __init__(
        self,
        connection: Connection,
        service: DiagramService,
        database_description: str,
        tables: DiagramDatabaseTables = None,
        metadata_reader: MetadataCollectionReader = None,
        service_reader: DiagramServiceReader = None,
        table_version: TableVersion = None
    ):
        tables = tables if tables is not None else DiagramDatabaseTables()
        super().__init__(
            connection,
            metadata_reader if metadata_reader is not None else MetadataCollectionReader(service, tables, connection),
            service_reader if service_reader is not None else DiagramServiceReader(service, tables, connection),
            service,
            database_description,
            table_version if table_version is not None else TableVersion()
        )
