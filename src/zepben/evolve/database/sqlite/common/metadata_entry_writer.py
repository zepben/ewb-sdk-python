#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
__all__ = ["MetadataEntryWriter"]

from zepben.evolve.database.sqlite.common.base_database_tables import BaseDatabaseTables
from zepben.evolve.database.sqlite.common.base_entry_writer import BaseEntryWriter
from zepben.evolve.database.sqlite.tables.table_metadata_data_sources import TableMetadataDataSources
from zepben.evolve.services.common.meta.data_source import DataSource

class MetadataEntryWriter(BaseEntryWriter):
    """
    A class for reading the `MetadataCollection` entries from the database.

    @param database_tables The tables that are available in the database.
    """

    def __init__(self, database_tables: BaseDatabaseTables):
        super().__init__()
        self._database_tables: BaseDatabaseTables = database_tables


    def save_data_source(self, data_source: DataSource) -> bool:
        """
        Save the `DataSource` fields to `TableMetadataDataSources`.

        @param data_source The `DataSource` to save to the database.

        @return true if the `DataSource` is successfully written to the database, otherwise false.
        """
        table = self._database_tables.get_table(TableMetadataDataSources)
        insert = self._database_tables.get_insert(TableMetadataDataSources)

        insert.add_value(table.source.query_index, data_source.source)
        insert.add_value(table.version.query_index, data_source.version)
        # The timestamp in the database uses Z for UTC while python uses +HH:mm format, so convert between them.
        insert.add_value(table.timestamp.query_index, f"{data_source.timestamp.isoformat()}Z")

        return insert.try_execute_single_update(lambda ex: insert.log_failure(self._logger, "data source", ex))
