#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
__all__ = ["MetadataEntryReader"]

import datetime
from typing import Callable

from zepben.evolve.database.sqlite.extensions.result_set import ResultSet
from zepben.evolve.database.sqlite.tables.table_metadata_data_sources import TableMetadataDataSources
from zepben.evolve.services.common.base_service import BaseService
from zepben.evolve.services.common.meta.data_source import DataSource


class MetadataEntryReader:
    """
    A class for reading the `MetadataCollection` entries from the database.

    :param service: The `BaseService` containing the `MetadataCollection` to populate from the database.
    """

    def __init__(self, service: BaseService):
        super().__init__()
        self._service: BaseService = service

    def load_metadata(self, table: TableMetadataDataSources, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        """
        Populate the `DataSource` fields from `TableMetadataDataSources`.
    
        :param table: The database table to read the `DataSource` fields from.
        :param result_set: The record in the database table containing the fields for this `DataSource`.
        :param set_identifier: A callback to set the identifier of the current row for logging purposes, which returns a copy of the provided string for
          fluent use.
    
        :return: True if the `DataSource` is successfully loaded from the database, otherwise False.
        """
        data_source = DataSource(
            set_identifier(result_set.get_string(table.source.query_index)),
            result_set.get_string(table.version.query_index),
            result_set.get_instant(table.timestamp.query_index, datetime.datetime(1970, 1, 1))
        )

        return self._service.metadata.add(data_source)
