#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["ChangeSetDatabaseWriter"]

import sqlite3
from pathlib import Path
from sqlite3 import Connection
from typing import Callable, Union

from zepben.ewb.database.sqlite.changeset.change_set_database_tables import ChangeSetDatabaseTables
from zepben.ewb.database.sqlite.changeset.change_set_service_writer import ChangeSetServiceWriter
from zepben.ewb.database.sqlite.common.base_database_writer import BaseDatabaseWriter
from zepben.ewb.database.sqlite.common.metadata_collection_writer import MetadataCollectionWriter
from zepben.ewb.services.variant.variant_service import VariantService


class ChangeSetDatabaseWriter(BaseDatabaseWriter):
    """
    A class for writing the `VariantService` objects and `MetadataCollection` to our change set database.

    :param database_file: the filename of the database to write.
    :param service: The `VariantService` to save to the database.
    """

    def __init__(
        self,
        database_file: Union[Path, str],
        service: VariantService,
        database_tables: ChangeSetDatabaseTables = None,
        create_metadata_writer: Callable[[], MetadataCollectionWriter] = None,
        create_service_writer: Callable[[], ChangeSetServiceWriter] = None,
        get_connection: Callable[[str], Connection] = None
    ):
        database_tables = database_tables if database_tables is not None else ChangeSetDatabaseTables()

        super().__init__(
            database_file,
            database_tables,
            create_metadata_writer if create_metadata_writer is not None else lambda: MetadataCollectionWriter(service, database_tables),
            create_service_writer if create_service_writer is not None else lambda: ChangeSetServiceWriter(service, database_tables),
            get_connection if get_connection is not None else sqlite3.connect
        )
