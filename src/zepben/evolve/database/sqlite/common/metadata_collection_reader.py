#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["MetadataCollectionReader"]

from sqlite3 import Connection

from zepben.evolve.database.sqlite.common.base_collection_reader import BaseCollectionReader
from zepben.evolve.database.sqlite.common.base_database_tables import BaseDatabaseTables
from zepben.evolve.database.sqlite.common.metadata_entry_reader import MetadataEntryReader
from zepben.evolve.database.sqlite.tables.table_metadata_data_sources import TableMetadataDataSources
from zepben.evolve.services.common.base_service import BaseService


class MetadataCollectionReader(BaseCollectionReader):
    """
    Class for reading the `MetadataCollection` from the database.

    :param service: The `BaseService` containing the `MetadataCollection` to populate from the database.
    :param tables: The tables available in the database.
    :param connection: The `Connection` to the database.
    """

    def __init__(
        self,
        service: BaseService,
        tables: BaseDatabaseTables,
        connection: Connection,
        reader: MetadataEntryReader = None
    ):
        super().__init__(tables, connection)
        self._reader: MetadataEntryReader = reader if reader is not None else MetadataEntryReader(service)

    def load(self) -> bool:
        return all([
            self._load_each(TableMetadataDataSources, self._reader.load_metadata)
        ])
