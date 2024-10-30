#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
__all__ = ["DiagramDatabaseWriter"]

import sqlite3
from pathlib import Path
from sqlite3 import Connection
from typing import Callable, Union

from zepben.evolve.database.sqlite.common.base_database_writer import BaseDatabaseWriter
from zepben.evolve.database.sqlite.common.metadata_collection_writer import MetadataCollectionWriter
from zepben.evolve.database.sqlite.diagram.diagram_database_tables import DiagramDatabaseTables
from zepben.evolve.database.sqlite.diagram.diagram_service_writer import DiagramServiceWriter
from zepben.evolve.services.diagram.diagrams import DiagramService


class DiagramDatabaseWriter(BaseDatabaseWriter):
    """
    A class for writing the `DiagramService` objects and `MetadataCollection` to our diagram database.

    :param database_file: the filename of the database to write.
    :param service: The `DiagramService` to save to the database.
    """

    def __init__(
        self,
        database_file: Union[Path, str],
        service: DiagramService,
        database_tables: DiagramDatabaseTables = None,
        create_metadata_writer: Callable[[], MetadataCollectionWriter] = None,
        create_service_writer: Callable[[], DiagramServiceWriter] = None,
        get_connection: Callable[[str], Connection] = None
    ):
        database_tables = database_tables if database_tables is not None else DiagramDatabaseTables()
        super().__init__(
            database_file,
            database_tables,
            create_metadata_writer if create_metadata_writer is not None else lambda: MetadataCollectionWriter(service, database_tables),
            create_service_writer if create_service_writer is not None else lambda: DiagramServiceWriter(service, database_tables),
            get_connection if get_connection is not None else sqlite3.connect
        )
