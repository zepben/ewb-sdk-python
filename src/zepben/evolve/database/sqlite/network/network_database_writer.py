#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import sqlite3
from pathlib import Path
from sqlite3 import Connection
from typing import Callable, Union

__all__ = ["NetworkDatabaseWriter"]

from zepben.evolve.database.sqlite.common.base_database_writer import BaseDatabaseWriter
from zepben.evolve.database.sqlite.common.metadata_collection_writer import MetadataCollectionWriter
from zepben.evolve.database.sqlite.network.network_database_tables import NetworkDatabaseTables
from zepben.evolve.database.sqlite.network.network_service_writer import NetworkServiceWriter
from zepben.evolve.services.network.network_service import NetworkService


class NetworkDatabaseWriter(BaseDatabaseWriter):
    """
    A class for writing the `NetworkService` objects and `MetadataCollection` to our network database.

    :param database_file: the filename of the database to write.
    :param service: The `NetworkService` to save to the database.
    """

    def __init__(
        self,
        database_file: Union[Path, str],
        service: NetworkService,
        database_tables: NetworkDatabaseTables = NetworkDatabaseTables(),
        create_metadata_writer: Callable[[Connection], MetadataCollectionWriter] = None,
        create_service_writer: Callable[[Connection], NetworkServiceWriter] = None,
        get_connection: Callable[[str], Connection] = None
    ):
        super().__init__(
            database_file,
            database_tables,
            create_metadata_writer if create_metadata_writer is not None else lambda: MetadataCollectionWriter(service, database_tables),
            create_service_writer if create_service_writer is not None else lambda: NetworkServiceWriter(service, database_tables),
            get_connection if get_connection is not None else sqlite3.connect
        )
